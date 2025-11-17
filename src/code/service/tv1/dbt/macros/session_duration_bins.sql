{% macro session_duration_group(duration_column) %}
CASE
    WHEN {{ duration_column }} = 0 THEN '0 min'
    {% for bound, label in [
        (1, '0–1 min'),
        (2, '1–2 min'),
        (3, '2–3 min'),
        (5, '3–5 min'),
        (10, '5–10 min'),
        (15, '10–15 min'),
        (20, '15–20 min'),
        (30, '20–30 min'),
        (40, '30–40 min'),
        (50, '40–50 min'),
        (60, '50–60 min'),
        (75, '60–75 min'),
        (90, '75–90 min'),
        (120, '90–120 min'),
        (150, '120–150 min'),
        (180, '150–180 min'),
        (210, '180–210 min'),
        (240, '210–240 min')
    ] %}
      WHEN {{ duration_column }} <= {{ bound }} THEN '{{ label }}'
    {% endfor %}
    ELSE '240+ min'
END
{% endmacro %}


{% macro session_duration_group_order(duration_column) %}
CASE
    WHEN {{ duration_column }} = 0 THEN 0
    {% for bound, i in [
        (1, 1),
        (2, 2),
        (3, 3),
        (5, 5),
        (10, 10),
        (15, 15),
        (20, 20),
        (30, 30),
        (40, 40),
        (50, 50),
        (60,  60),
        (75, 75),
        (90, 90),
        (120, 120),
        (150, 150),
        (180, 180),
        (210, 210),
        (240, 240)
    ] %}
      WHEN {{ duration_column }} <= {{ bound }} THEN {{ i }}
    {% endfor %}
    ELSE {{ 300 }}
END
{% endmacro %}
