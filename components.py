"""Reusable Streamlit components for displaying health indicators."""

from html import escape

import pandas as pd
import streamlit as st


def load_indicator_styles():
    st.markdown(
        """
        <style>
        .st-key-dashboard-container {
            padding: 1rem !important;
        }
        .st-key-health-indicators-panel {
            padding: 0.65rem !important;
        }
        div[data-testid="stMetricLabel"] p {
            font-size: 0.9rem;
        }
        div[data-testid="stMetricValue"] {
            font-size: 1.45rem;
        }
        .indicator-feedback {
            min-height: 3.25rem;
            width: 100%;
            box-sizing: border-box;
            display: flex;
            align-items: center;
            padding: 0.55rem;
            border-radius: 0.4rem;
            font-size: 0.875rem;
            line-height: 1.35;
            background: rgba(127, 127, 127, 0.08);
            border-left: 0.25rem solid #6b8f9e;
        }
        .indicator-feedback span {
            display: block;
        }
        .indicator-status {
            font-size: 0.9rem;
            font-weight: 600;
        }
        .dashboard-timeline-item {
            margin: 0.45rem 0;
            padding: 0.55rem 0.7rem;
            border-left: 0.2rem solid #6b8f9e;
            border-radius: 0 0.45rem 0.45rem 0;
            background: rgba(127, 127, 127, 0.08);
        }
        .dashboard-timeline-heading {
            display: flex;
            justify-content: space-between;
            gap: 0.5rem;
            font-size: 0.9rem;
            font-weight: 600;
        }
        .dashboard-timeline-time {
            font-size: 0.8rem;
            font-weight: 400;
            opacity: 0.75;
            white-space: nowrap;
        }
        .dashboard-timeline-context {
            margin-top: 0.15rem;
            font-size: 0.92rem;
        }
        .dashboard-timeline-detail {
            margin-top: 0.15rem;
            font-size: 0.85rem;
            opacity: 0.75;
        }
        @media (max-width: 900px) {
            .st-key-dashboard-container {
                padding: 0.65rem !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def display_indicator_status(color, status, messages):
    range_label = (
        "Within the app's generic reference range"
        if status == "normal"
        else "Outside the app's generic reference range"
    )
    st.markdown(
        f"<span class='indicator-status'>{range_label}</span>",
        unsafe_allow_html=True,
    )
    message = messages[status]
    st.markdown(
        f"<div class='indicator-feedback' "
        f"title='{escape(message, quote=True)}' role='status'>"
        f"<span>{escape(message)}</span></div>",
        unsafe_allow_html=True,
    )


def display_indicator_card(
    label, value, color, status, messages, explanation=None
):
    with st.container(border=True):
        st.metric(label=label, value=value)
        if status is None:
            st.caption(
                "No reading yet"
                if value == "—"
                else "No generic category applied for this context"
            )
        else:
            display_indicator_status(color, status, messages)
        if explanation:
            text, source_label, source_url = explanation
            with st.expander("Why measure this?"):
                st.write(text)
                st.markdown(f"[{source_label}]({source_url})")


def display_dashboard_timeline_event(event_type, timestamp, context, detail):
    icons = {
        "Health check-in": "🩺",
        "Activity": "🏃",
        "Well-being check-in": "🙂",
        "Sleep": "🌙",
    }
    title = escape(str(event_type))
    icon = icons.get(event_type, "📌")
    context_text = escape(str(context or ""))
    detail_text = escape(str(detail or ""))
    detail_markup = (
        f"<div class='dashboard-timeline-detail'>{detail_text}</div>"
        if detail_text
        else ""
    )
    st.markdown(
        f"<div class='dashboard-timeline-item'>"
        f"<div class='dashboard-timeline-heading'>"
        f"<span>{icon} {title}</span>"
        f"<span class='dashboard-timeline-time'>{escape(str(timestamp))}</span>"
        f"</div>"
        f"<div class='dashboard-timeline-context'>{context_text}</div>"
        f"{detail_markup}</div>",
        unsafe_allow_html=True,
    )


def display_timeline_event(event_type, timestamp, context, metrics, details):
    icons = {
        "Health check-in": "🩺",
        "Activity": "🏃",
        "Well-being check-in": "🙂",
        "Sleep": "🌙",
    }

    with st.container(border=True):
        title_column, timestamp_column = st.columns([1, 1])
        with title_column:
            st.markdown(f"#### {icons.get(event_type, '📌')} {event_type}")
        with timestamp_column:
            st.caption(timestamp)

        if context:
            st.caption(f"Context: {context}")

        if metrics:
            metric_columns = st.columns(min(len(metrics), 4))
            for index, (label, value) in enumerate(metrics):
                with metric_columns[index % len(metric_columns)]:
                    st.metric(label=label, value=value)

        visible_details = [
            (label, value)
            for label, value in details
            if value is not None and not pd.isna(value) and str(value).strip()
        ]
        if visible_details:
            with st.expander("More details"):
                for label, value in visible_details:
                    st.markdown(f"**{label}:** {value}")