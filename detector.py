import cv2
import numpy as np


def detect_layers(image):

    if image is None:
        return 0, image

    # =========================================================
    # 1. PREPARE IMAGE
    # =========================================================

    image = cv2.resize(image, (600, 600))
    result = image.copy()

    h, w = image.shape[:2]

    # =========================================================
    # 2. COLOR SPACES
    # =========================================================

    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    L, A, B = cv2.split(lab)
    H, S, V = cv2.split(hsv)

    # Convert to float
    L = L.astype(np.float32)
    A = A.astype(np.float32)
    S = S.astype(np.float32)

    # =========================================================
    # 3. LIGHTING NORMALIZATION
    #
    # Remove VERY slow illumination changes.
    #
    # Example:
    #
    # left side = bright
    # right side = dark
    #
    # This shouldn't be mistaken for a layer.
    # =========================================================

    background = cv2.GaussianBlur(
        L,
        (0, 0),
        45
    )

    normalized_L = L - background

    # =========================================================
    # 4. LOCAL CONTRAST
    #
    # This is the important part for LIGHT onions.
    #
    # We compare small-scale changes instead of absolute
    # brightness.
    # =========================================================

    small_L = cv2.GaussianBlur(
        L,
        (0, 0),
        2
    )

    medium_L = cv2.GaussianBlur(
        L,
        (0, 0),
        7
    )

    brightness_detail = (
        small_L - medium_L
    )

    # Color detail
    small_A = cv2.GaussianBlur(
        A,
        (0, 0),
        2
    )

    medium_A = cv2.GaussianBlur(
        A,
        (0, 0),
        7
    )

    red_detail = (
        small_A - medium_A
    )

    # Saturation detail
    small_S = cv2.GaussianBlur(
        S,
        (0, 0),
        2
    )

    medium_S = cv2.GaussianBlur(
        S,
        (0, 0),
        7
    )

    saturation_detail = (
        small_S - medium_S
    )

    # =========================================================
    # 5. GRADIENTS
    #
    # Detect sharp transitions.
    # =========================================================

    gx_L = cv2.Sobel(
        L,
        cv2.CV_32F,
        1,
        0,
        ksize=3
    )

    gy_L = cv2.Sobel(
        L,
        cv2.CV_32F,
        0,
        1,
        ksize=3
    )

    gradient_L = cv2.magnitude(
        gx_L,
        gy_L
    )

    gx_A = cv2.Sobel(
        A,
        cv2.CV_32F,
        1,
        0,
        ksize=3
    )

    gy_A = cv2.Sobel(
        A,
        cv2.CV_32F,
        0,
        1,
        ksize=3
    )

    gradient_A = cv2.magnitude(
        gx_A,
        gy_A
    )

    gx_S = cv2.Sobel(
        S,
        cv2.CV_32F,
        1,
        0,
        ksize=3
    )

    gy_S = cv2.Sobel(
        S,
        cv2.CV_32F,
        0,
        1,
        ksize=3
    )

    gradient_S = cv2.magnitude(
        gx_S,
        gy_S
    )

    # =========================================================
    # 6. NORMALIZE EACH SIGNAL
    #
    # Percentile normalization prevents one strong feature
    # from dominating everything.
    # =========================================================

    def normalize_signal(signal):

        low = np.percentile(
            signal,
            10
        )

        high = np.percentile(
            signal,
            95
        )

        if high - low < 1e-6:
            return np.zeros_like(signal)

        signal = (
            signal - low
        ) / (
            high - low
        )

        return np.clip(
            signal,
            0,
            1
        )

    gradient_L = normalize_signal(
        gradient_L
    )

    gradient_A = normalize_signal(
        gradient_A
    )

    gradient_S = normalize_signal(
        gradient_S
    )

    # =========================================================
    # 7. COMBINE COLOR + BRIGHTNESS BOUNDARIES
    # =========================================================

    boundary_map = (
        0.45 * gradient_L +
        0.35 * gradient_A +
        0.20 * gradient_S
    )

    # =========================================================
    # 8. RADIAL ANALYSIS
    #
    # We still use rays, but NOT circles as a requirement.
    #
    # Every direction gets its own boundary profile.
    # =========================================================

    cx = w // 2
    cy = h // 2

    max_radius = min(
        cx,
        cy
    ) - 20

    radii = np.arange(
        15,
        max_radius
    )

    # Fewer rays = faster
    angles = np.linspace(
        0,
        2 * np.pi,
        240,
        endpoint=False
    )

    radial_profiles = []

    for angle in angles:

        cos_a = np.cos(angle)
        sin_a = np.sin(angle)

        xs = (
            cx +
            radii * cos_a
        ).astype(np.int32)

        ys = (
            cy +
            radii * sin_a
        ).astype(np.int32)

        valid = (
            (xs >= 0) &
            (xs < w) &
            (ys >= 0) &
            (ys < h)
        )

        profile = np.zeros(
            len(radii),
            dtype=np.float32
        )

        profile[valid] = boundary_map[
            ys[valid],
            xs[valid]
        ]

        radial_profiles.append(
            profile
        )

    radial_profiles = np.array(
        radial_profiles,
        dtype=np.float32
    )

    # =========================================================
    # 9. SUPPRESS ISOLATED NOISE
    #
    # A real onion boundary should usually appear in several
    # neighboring directions.
    # =========================================================

    radial_profiles = cv2.GaussianBlur(
        radial_profiles,
        (1, 5),
        0
    )

    # =========================================================
    # 10. BOUNDARY EVIDENCE
    #
    # Instead of median, use multiple statistics.
    #
    # 50th percentile = fairly common
    # 75th percentile = stronger evidence
    # maximum = detects partially visible boundaries
    # =========================================================

    p50 = np.percentile(
        radial_profiles,
        50,
        axis=0
    )

    p75 = np.percentile(
        radial_profiles,
        75,
        axis=0
    )

    p90 = np.percentile(
        radial_profiles,
        90,
        axis=0
    )

    boundary_score = (
        0.40 * p50 +
        0.40 * p75 +
        0.20 * p90
    )

    # =========================================================
    # 11. NORMALIZE FINAL PROFILE
    # =========================================================

    low = np.percentile(
        boundary_score,
        20
    )

    high = np.percentile(
        boundary_score,
        95
    )

    if high - low > 1e-6:

        boundary_score = (
            boundary_score - low
        ) / (
            high - low
        )

    boundary_score = np.clip(
        boundary_score,
        0,
        1
    )

    # Smooth only slightly
    boundary_score = cv2.GaussianBlur(
        boundary_score.reshape(-1, 1),
        (1, 7),
        0
    ).flatten()

    # =========================================================
    # 12. PEAK DETECTION
    # =========================================================

    candidates = []

    for i in range(
        6,
        len(boundary_score) - 6
    ):

        current = boundary_score[i]

        # Local maximum
        local = boundary_score[
            i - 5:i + 6
        ]

        if current != np.max(local):
            continue

        # Adaptive local threshold
        surrounding = np.concatenate([
            boundary_score[
                i - 12:i - 6
            ],
            boundary_score[
                i + 7:i + 13
            ]
        ])

        local_mean = np.mean(
            surrounding
        )

        local_std = np.std(
            surrounding
        )

        # Peak must stand above its surroundings
        prominence = (
            current -
            local_mean
        )

        if (
            current > 0.28
            and
            prominence >
            max(
                0.035,
                0.45 * local_std
            )
        ):

            candidates.append(i)

    # =========================================================
    # 13. MERGE NEARBY PEAKS
    # =========================================================

    candidates = sorted(
        candidates,
        key=lambda i: boundary_score[i],
        reverse=True
    )

    selected = []

    minimum_spacing = 10

    for index in candidates:

        radius = int(
            radii[index]
        )

        if radius < 25:
            continue

        too_close = False

        for selected_index in selected:

            selected_radius = int(
                radii[selected_index]
            )

            if abs(
                radius -
                selected_radius
            ) < minimum_spacing:

                too_close = True
                break

        if not too_close:

            selected.append(index)

    # Sort inside → outside
    selected.sort()

    # =========================================================
    # 14. REASONABLE RANGE
    # =========================================================

    detected_radii = [
        int(radii[i])
        for i in selected
    ]

    # Onion usually doesn't have dozens of visible boundaries.
    detected_radii = detected_radii[:10]

    layer_count = len(
        detected_radii
    )

    # =========================================================
    # 15. NO GREEN CIRCLES
    #
    # We deliberately DON'T draw the detected radii.
    # =========================================================

    cv2.putText(
        result,
        f"Layers: {layer_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    return layer_count, result