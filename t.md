Okay, acting as a Financial Data Scientist, let's focus solely on the calculations (conceptually) and visualizations within Power BI, assuming the data is already cleaned and structured as discussed previously.

**Assumed Clean Data Structure:**

| L2_Department | Quarter | Year | Quarter_Num | Quarter_Sortable | Review_Name | Risk_Category_L3 | Detailed_Risk_L3                                                    | Region/Entity | Primary_Location | Risk_Category_L2                            | Location_Country | Unique_ID |
| :------------ | :------ | :--- | :---------- | :--------------- | :---------- | :--------------- | :------------------------------------------------------------------ | :------------ | :--------------- | :------------------------------------------ | :--------------- | :-------- |
| L2C DFIN/CTL  | 2025 Q1 | 2025 | 1           | 2025-Q1          | HR          | Account... IFRS 2 | Breach of regulatory...                                             | SG            | HONG KONG        | Compliance... dispute...                      | HONG KONG        | 1         |
| L2C DFIN/CTL  | 2025 Q1 | 2025 | 1           | 2025-Q1          | HR          | Account... IFRS 2 | Breach of regulatory...                                             | SG            | MUMBAI           | Compliance... dispute...                      | INDIA            | 2         |
| L2C DFIN/CTL  | 2025 Q1 | 2025 | 1           | 2025-Q1          | HR          | Account... IFRS 2 | Breach of regulatory...                                             | SG            | SINGAPORE        | Compliance... dispute...                      | SINGAPORE        | 3         |
| L2C DFIN/CTL  | 2025 Q1 | 2025 | 1           | 2025-Q1          | HR          | Account... IFRS 2 | Breach of regulatory...                                             | SG            | TAIPEI           | Compliance... dispute...                      | TAIWAN           | 4         |

*(Includes conceptual columns like Year, Quarter_Num, Unique_ID for analysis)*

**Phase 1: Calculation Concepts (Measures & Calculated Columns - No DAX Syntax)**

We will leverage Power BI's ability to create implicit measures (automatic aggregations) and define concepts for more explicit measures or columns needed for advanced analysis.

1.  **Core Metric - Risk Instance Count:**
    *   **Concept:** The fundamental measure is the count of individual risk records identified.
    *   **Calculation:** Count the number of rows or, more robustly, the distinct count of the `Unique_ID` column. Power BI does this implicitly when you use `Unique_ID` in the 'Values' field of many visuals and select 'Count' or 'Count (Distinct)'. Let's call this `Risk Count`.

2.  **Dimension Uniqueness Counts:**
    *   **Concept:** Understand the breadth of the risk landscape across key categories.
    *   **Calculations:**
        *   `Number of Impacted Locations`: Distinct count of `Location_Country` or `Primary_Location`.
        *   `Number of L2 Risk Categories`: Distinct count of `Risk_Category_L2`.
        *   `Number of L3 Risk Categories`: Distinct count of `Risk_Category_L3`.
        *   `Number of Departments`: Distinct count of `L2_Department`.
    *   **Power BI:** Use Card visuals, drag the respective column, and set summarization to 'Count (Distinct)'.

3.  **Proportional Analysis (Conceptual - requires explicit measures usually):**
    *   **Concept:** Understand the relative contribution of different categories to the total risk count.
    *   **Calculations:**
        *   `% of Total Risks by Location`: ([Risk Count for a specific Location] / [Risk Count for ALL Locations]) * 100.
        *   `% of Total Risks by L2 Category`: ([Risk Count for a specific L2 Category] / [Risk Count for ALL L2 Categories]) * 100.
    *   **Power BI:** While this often requires simple DAX measures, the *concept* can be visualized using visuals that show proportions like Treemaps or 100% Stacked Bar/Column charts, where Power BI handles the percentage calculation visually.

4.  **Time-Based Calculations (Conceptual - requires explicit measures & date table):**
    *   **Concept:** Analyze trends over time (though our sample is only one quarter). With more data, this is crucial.
    *   **Calculations:**
        *   `Risk Count Previous Quarter`: The `Risk Count` calculated for the preceding quarter.
        *   `Quarter-over-Quarter Risk Count Change %`: The percentage difference between `Risk Count` and `Risk Count Previous Quarter`.
    *   **Power BI:** Requires a dedicated Calendar/Date table and Time Intelligence functions (conceptually). Visualized using Line Charts or clustered charts comparing periods.

**Phase 2: Advanced Visualizations and Analysis**

Let's design report pages focusing on leveraging Power BI's more advanced capabilities.

**Report Page 1: Risk Landscape Overview**

*   **Objective:** Provide a high-level summary of the risk profile and key concentrations.
*   **Visualizations:**
    1.  **Cards (KPIs):**
        *   Display `Risk Count` (Total Instances).
        *   Display `Number of Impacted Locations` (Distinct Count of `Location_Country`).
        *   Display `Number of L2 Risk Categories` (Distinct Count of `Risk_Category_L2`).
        *   Display `Number of Departments` (Distinct Count of `L2_Department`).
    2.  **Filled Map / Bubble Map (Advanced Geographic):**
        *   **Location:** `Location_Country`.
        *   **Bubble Size / Color Saturation:** `Risk Count` (implicit count of `Unique_ID`).
        *   **Tooltips:** Add `Primary_Location`, `Risk_Category_L2`, `Risk_Category_L3`, `Risk Count`.
        *   **Insight:** Immediately shows the geographic distribution and concentration of risks. Highlights countries with the highest volume. Bubble map is good if counts vary significantly; Filled Map for regional presence.
    3.  **Treemap (Proportional Analysis):**
        *   **Category:** `Risk_Category_L2`. (Can add `Risk_Category_L3` for drill-down).
        *   **Values:** `Risk Count`.
        *   **Insight:** Visually represents the proportion of total risks attributed to each L2 category. Larger rectangles indicate dominant risk types. In our sample, it would show 100% for "Compliance...".
    4.  **Slicers:**
        *   Include slicers for `Quarter_Sortable`, `Location_Country`, `L2_Department`. Allows interactive filtering of the entire page.

**Report Page 2: Deep Dive Analysis (Interactive Exploration)**

*   **Objective:** Allow users to explore relationships and drill down into specific risk drivers.
*   **Visualizations:**
    1.  **Decomposition Tree (Advanced AI Visual):**
        *   **Analyze:** `Risk Count`.
        *   **Explain By:** Add dimensions in likely order of exploration: `L2_Department`, `Risk_Category_L2`, `Risk_Category_L3`, `Location_Country`, `Primary_Location`, `Review_Name`.
        *   **Insight:** This is the star for exploration. Users can click through different paths (e.g., start with Department -> L2 Risk -> Location) to see how the total risk count breaks down. AI features can suggest interesting splits. For the sample, it would show a simple path, but with real data, it reveals complex interactions.
    2.  **Matrix with Conditional Formatting (Advanced Cross-Tabulation):**
        *   **Rows:** Use a hierarchy: `Risk_Category_L2` -> `Risk_Category_L3`.
        *   **Columns:** Use a hierarchy: `Location_Country` -> `Primary_Location`.
        *   **Values:** `Risk Count`.
        *   **Conditional Formatting:** Apply 'Background color scales' (Heatmap) to the `Risk Count` values. Darker colors indicate higher risk counts.
        *   **Insight:** Creates a heatmap showing hotspots – combinations of Risk Categories and Locations with high frequencies. Excellent for identifying systemic issues vs. localized ones.
    3.  **Table (Detailed View):**
        *   **Columns:** `Detailed_Risk_L3`, `Primary_Location`, `Location_Country`, `Review_Name`, `Quarter_Sortable`.
        *   **Function:** Acts as a detail view that gets filtered when users interact with the Decomposition Tree, Map, or Matrix. Provides the granular text and context for selected risk instances.

**Report Page 3: (Optional - If Text Varies) Risk Theme Analysis**

*   **Objective:** Identify recurring themes or keywords within the detailed risk descriptions.
*   **Visualizations:**
    1.  **Word Cloud (Custom Visual):**
        *   **Category:** `Detailed_Risk_L3` (or potentially combine L3 and Detailed L3).
        *   **Values:** `Risk Count`.
        *   **Insight:** If the `Detailed_Risk_L3` descriptions had more variation, this visual would highlight the most frequently occurring words or short phrases, potentially revealing underlying themes not captured by the L2/L3 categories alone. *Requires importing the visual from AppSource.*
    2.  **Filtered Table:** A table showing the full `Detailed_Risk_L3` descriptions, filtered by selections in other visuals or slicers.

**Interactivity Strategy:**

*   **Cross-Filtering:** Ensure visuals on the same page interact (clicking a country on the map filters the matrix and decomposition tree, etc.). This is default but crucial.
*   **Slicers:** Provide global filters (like Quarter/Year) that affect multiple pages or targeted filters on specific pages.
*   **Drill-Through:** Could set up drill-through from the Overview map/treemap to the Deep Dive page, passing the selected context (e.g., drill through from a specific L2 Risk Category).
*   **Tooltips:** Customize tooltips on the Map, Treemap, and Matrix to show relevant additional details on hover without cluttering the main visual. Could even use *report page tooltips* for mini-dashboards on hover.

**Insights from Sample Data using these Visuals:**

1.  **Map:** Would show markers/color intensity equally across Hong Kong, India, Singapore, Taiwan, indicating the risk appeared in all these locations in 2025 Q1.
2.  **Treemap:** Would be a single rectangle for "Compliance and other dispute with authorities", occupying 100% of the area.
3.  **Decomposition Tree:** Would show a simple split: Total (4) -> L2C DFIN/CTL (4) -> Compliance... (4) -> Breach of regulatory... (4) -> then splitting evenly by Location (1 each).
4.  **Matrix:** Would show a '1' in the cells corresponding to the single L2/L3 risk combination for each of the four locations. The heatmap (if scaled automatically) might show all these cells in the same color.

This plan leverages standard and advanced Power BI features to move beyond simple reporting towards interactive exploration and insight generation, even with limited initial data variety. The techniques scale effectively as more diverse and voluminous data becomes available.