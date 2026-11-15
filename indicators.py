"""Shared health-indicator fields, thresholds, messages, and evaluators."""

STATUS_COLORS = {"normal": "green", "warning": "orange", "critical": "red"}

CHECKIN_FIELDS = (
    "bpm",
    "spo2",
    "systolic",
    "diastolic",
    "temperature",
)

CHECKIN_OPTIONAL_FIELDS = (
    "measurement_context",
    "measurement_source",
    "symptoms",
    "observation",
    "radiation",
    "radiation_source",
)

THRESHOLDS = {
    "oxygen": {"normal_min": 95, "warning_min": 90},
    "heart_rate": {
        "normal_min": 60,
        "normal_max": 100,
        "warning_min": 50,
        "warning_max": 110,
    },
    "blood_pressure": {
        "critical_systolic": 140,
        "critical_diastolic": 90,
        "normal_systolic_max": 120,
        "normal_diastolic_max": 80,
        "warning_systolic_max": 140,
        "warning_diastolic_max": 90,
        "elevated_systolic_max": 130,
    },
    "temperature": {
        "normal_min": 36.1,
        "normal_max": 37.2,
        "warning_max": 38.0,
    },
    "hydration": {"normal_min": 60, "warning_min": 50},
    "calories": {
        "normal_min": 2000,
        "normal_max": 2500,
        "warning_min": 1500,
        "warning_max": 3000,
    },
    "sleep": {
        "normal_min": 7,
        "normal_max": 9,
        "warning_min": 6,
        "warning_max": 10,
    },
}

INDICATOR_MESSAGES = {
    "oxygen": {
        "normal": "Generic prototype reference only; not a clinical threshold or diagnosis.",
        "warning": "Generic prototype reference only; not a clinical threshold or diagnosis.",
        "critical": "Generic prototype reference only; not a clinical threshold or diagnosis.",
    },
    "heart_rate": {
        "normal": "Generic prototype reference only; not a clinical threshold or diagnosis.",
        "warning": "Generic prototype reference only; not a clinical threshold or diagnosis.",
        "critical": "Generic prototype reference only; not a clinical threshold or diagnosis.",
    },
    "blood_pressure": {
        "normal": "Generic prototype reference only; not a clinical threshold or diagnosis.",
        "warning": "Generic prototype reference only; not a clinical threshold or diagnosis.",
        "critical": "Generic prototype reference only; not a clinical threshold or diagnosis.",
    },
    "temperature": {
        "normal": "Generic prototype reference only; not a clinical threshold or diagnosis.",
        "warning": "Generic prototype reference only; not a clinical threshold or diagnosis.",
        "critical": "Generic prototype reference only; not a clinical threshold or diagnosis.",
    },
    "hydration": {
        "normal": "Generic prototype reference only; not a clinical threshold or diagnosis.",
        "warning": "Generic prototype reference only; not a clinical threshold or diagnosis.",
        "critical": "Generic prototype reference only; not a clinical threshold or diagnosis.",
    },
    "calories": {
        "normal": "Generic prototype reference only; not a clinical threshold or diagnosis.",
        "warning": "Generic prototype reference only; not a clinical threshold or diagnosis.",
        "critical": "Generic prototype reference only; not a clinical threshold or diagnosis.",
    },
    "sleep": {
        "normal": "Generic prototype reference only; not a clinical threshold or diagnosis.",
        "warning": "Generic prototype reference only; not a clinical threshold or diagnosis.",
        "critical": "Generic prototype reference only; not a clinical threshold or diagnosis.",
    },
    "radiation": {
        "normal": "Generic prototype reference only; not a clinical threshold or diagnosis.",
        "warning": "Generic prototype reference only; not a clinical threshold or diagnosis.",
        "critical": "Generic prototype reference only; not a clinical threshold or diagnosis.",
    },
}

WHY_MEASURE = {
    "oxygen": (
        "NASA identifies hypoxia as a risk in future exploration missions. "
        "This SpO2 entry is a recorded value, not a diagnosis or mission threshold.",
        "NASA: Risk of Hypoxia",
        "https://www.nasa.gov/reference/risk-of-hypoxia/",
    ),
    "heart_rate": (
        "NASA notes that spaceflight can affect cardiovascular function. "
        "Recording whether a reading was at rest, during activity, or after exercise "
        "helps keep comparisons in context.",
        "NASA: Cardiovascular Adaptations",
        "https://www.nasa.gov/directorates/esdmd/hhp/cv-risk/",
    ),
    "blood_pressure": (
        "NASA studies cardiovascular changes associated with spaceflight. "
        "This log preserves readings over time; it does not assess risk or diagnose.",
        "NASA: Cardiovascular Adaptations",
        "https://www.nasa.gov/directorates/esdmd/hhp/cv-risk/",
    ),
    "temperature": (
        "NASA identifies habitat temperature control as a closed-environment concern. "
        "This body-temperature entry is separate from spacecraft environmental "
        "monitoring.",
        "NASA: Hostile/Closed Environments",
        "https://www.nasa.gov/hrp/hazard-hostile-closed-environments/",
    ),
    "activity": (
        "NASA studies exercise as a way to help maintain cardiorespiratory and "
        "musculoskeletal fitness during spaceflight. This log records activity; "
        "it is not an exercise prescription.",
        "NASA: Reduced Fitness Risk",
        "https://www.nasa.gov/reference/risk-of-reduced-cardiorespiratory-and-musculoskeletal-fitness/",
    ),
    "wellbeing": (
        "NASA identifies isolation and confinement as behavioral-health challenges. "
        "Mood, stress, and isolation are separate self-reports in this prototype.",
        "NASA: Isolation and Confinement",
        "https://www.nasa.gov/hrp/hazard-isolation-and-confinement/",
    ),
    "sleep": (
        "NASA notes that sleep loss and circadian disruption can affect performance "
        "in isolated missions. These records show reported periods and quality, not "
        "a clinical sleep assessment.",
        "NASA: Isolation and Confinement",
        "https://www.nasa.gov/hrp/hazard-isolation-and-confinement/",
    ),
}

# Keep the previous name available to callers that already use it.
colors = STATUS_COLORS


def has_resting_heart_rate_context(context):
    return context == "At rest"


def oxigen_saturation_indicator(value):
    limits = THRESHOLDS["oxygen"]
    if value >= limits["normal_min"]:
        status = "normal"
    elif value >= limits["warning_min"]:
        status = "warning"
    else:
        status = "critical"
    return STATUS_COLORS[status], status


def heart_rate_indicator(value):
    limits = THRESHOLDS["heart_rate"]
    if limits["normal_min"] <= value <= limits["normal_max"]:
        status = "normal"
    elif limits["warning_min"] <= value <= limits["warning_max"]:
        status = "warning"
    else:
        status = "critical"
    return STATUS_COLORS[status], status


def pressure_indicator(systolic, diastolic):
    limits = THRESHOLDS["blood_pressure"]
    if (
        systolic >= limits["critical_systolic"]
        or diastolic >= limits["critical_diastolic"]
    ):
        status = "critical"
    elif (
        systolic < limits["normal_systolic_max"]
        and diastolic < limits["normal_diastolic_max"]
    ):
        status = "normal"
    elif (
        limits["normal_systolic_max"] <= systolic < limits["elevated_systolic_max"]
        and diastolic < limits["normal_diastolic_max"]
    ) or (
        limits["elevated_systolic_max"] <= systolic < limits["warning_systolic_max"]
    ) or (
        limits["normal_diastolic_max"] <= diastolic < limits["warning_diastolic_max"]
    ):
        status = "warning"
    else:
        status = "critical"
    return STATUS_COLORS[status], status


def temperature_indicator(value):
    limits = THRESHOLDS["temperature"]
    if limits["normal_min"] <= value <= limits["normal_max"]:
        status = "normal"
    elif limits["normal_max"] < value <= limits["warning_max"]:
        status = "warning"
    else:
        status = "critical"
    return STATUS_COLORS[status], status


def hydration_indicator(value):
    limits = THRESHOLDS["hydration"]
    if value >= limits["normal_min"]:
        status = "normal"
    elif value >= limits["warning_min"]:
        status = "warning"
    else:
        status = "critical"
    return STATUS_COLORS[status], status


def calories_indicator(value):
    limits = THRESHOLDS["calories"]
    if limits["normal_min"] <= value <= limits["normal_max"]:
        status = "normal"
    elif (
        limits["warning_min"] <= value < limits["normal_min"]
        or limits["normal_max"] < value <= limits["warning_max"]
    ):
        status = "warning"
    else:
        status = "critical"
    return STATUS_COLORS[status], status


def sleep_hours_indicator(value):
    limits = THRESHOLDS["sleep"]
    if limits["normal_min"] <= value <= limits["normal_max"]:
        status = "normal"
    elif (
        limits["warning_min"] <= value < limits["normal_min"]
        or limits["normal_max"] < value <= limits["warning_max"]
    ):
        status = "warning"
    else:
        status = "critical"
    return STATUS_COLORS[status], status
