# Databank visual standard

## Purpose

Databank presentation follows one analytical design logic across Streamlit,
exported analytical exhibits, Excel and future PowerPoint use. The priority is
clear evidence, not decorative interface treatment.

## Foundation

- Typeface: Arial only.
- Canvas and body text: white `#FFFFFF`, black or near-black body text.
- Primary structural colour: Thursday Purple `#412B48`.
- Selective accent/warning: Dark Red `#842044`; Cognac `#B25F4D` only when a
  second analytical distinction is useful.
- Separation: light grey `#EEEEEE`; use borders and whitespace rather than
  shadows, rounded SaaS cards or decoration.
- Use one or two dominant colours in an exhibit unless additional colours have
  a genuine analytical role.

## Streamlit pages and exhibits

Analytical pages use: small context, page title, short purpose, controls, then
analysis. Section headings are compact and left-aligned. KPI cards are white,
compact, purple-accented, with a fully visible label and a dominant value.
Warnings use the shared restrained red callout.

Charts use the shared Plotly formatter: white background, Arial, purple focal
series, horizontal light-grey gridlines, compact margins and descriptive titles.
Charts must carry their title and necessary unit/context inside the figure so a
PNG remains interpretable outside the application.

## Tables and Excel

Tables keep analytical values numeric and show missing observations as blank or
an explicit UI dash, never zero. User-facing columns use Danish labels. Excel
uses Arial 10pt, hidden gridlines, compact rows, purple headers with white bold
text, freeze panes, deliberate widths and number formats that display zero as
`-` and negatives in red parentheses. Consulting-facing tables are separated
from technical metadata.

## Output and PowerPoint readiness

Plotly modebar PNG export is standardised to 1600×900 with a deterministic
filename. The white, titled chart can be inserted directly in a 16:9 Thursday
PowerPoint. Native PowerPoint generation remains a later enhancement once an
approved Thursday PowerPoint master/template is supplied.
