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
    "radiation": {"normal_max": 1.0, "warning_max": 3.0},
}

INDICATOR_MESSAGES = {
    "oxygen": {
        "normal": "Oxygen saturation is within the normal range.",
        "warning": "Oxygen saturation is slightly low. Monitor your health.",
        "critical": "Low oxygen saturation! Seek medical attention.",
    },
    "heart_rate": {
        "normal": "Heart rate is within the normal range.",
        "warning": "Heart rate is slightly abnormal. Monitor your health.",
        "critical": "Abnormal heart rate! Seek medical attention.",
    },
    "blood_pressure": {
        "normal": "Blood pressure is within the normal range.",
        "warning": "Blood pressure is slightly elevated. Monitor your health.",
        "critical": "High blood pressure! Seek medical attention.",
    },
    "temperature": {
        "normal": "Body temperature is within the normal range.",
        "warning": "Body temperature is slightly elevated. Monitor your health.",
        "critical": "Abnormal body temperature! Seek medical attention.",
    },
    "hydration": {
        "normal": "Hydration level is within the normal range.",
        "warning": "Hydration level is low. Increase water intake.",
        "critical": "Hydration level is critically low. Seek medical attention.",
    },
    "calories": {
        "normal": "Calorie intake is within the target range.",
        "warning": "Calorie intake is outside the target range. Monitor your intake.",
        "critical": "Calorie intake is far outside the target range.",
    },
    "sleep": {
        "normal": "Sleep duration is within the normal range.",
        "warning": "Sleep duration is outside the recommended range. Monitor your sleep.",
        "critical": "Insufficient or excessive sleep duration. Review your sleep habits.",
    },
    "radiation": {
        "normal": "Radiation exposure is within the normal range.",
        "warning": "Radiation exposure is slightly high. Monitor your exposure.",
        "critical": "High radiation exposure! Seek medical attention.",
    },
}

# Keep the previous name available to callers that already use it.
colors = STATUS_COLORS


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


def radiation_indicator(value):
    limits = THRESHOLDS["radiation"]
    if value < limits["normal_max"]:
        status = "normal"
    elif value < limits["warning_max"]:
        status = "warning"
    else:
        status = "critical"
    return STATUS_COLORS[status], status