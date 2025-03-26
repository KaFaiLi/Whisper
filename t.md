Okay, building on the previous analysis, let's add a couple more sophisticated calculations in Power Query that can provide deeper insights, particularly relevant for risk management.

**Calculation 6: Identify Repeat Risks**

*   **Purpose:** To flag specific risks (`L3risks`) that are recurring within the same `Location`. Identifying repeat findings is crucial as it might indicate ineffective remediation of previously identified issues or systemic problems.
*   **Method (Power Query):**
    1.  **Create a Unique Key:** We need a key that identifies a specific risk in a specific location.
        *   Go to 'Add Column' -> 'Custom Column'.
        *   New column name: `RiskLocationKey`
        *   Formula: `[L3risks] & "|" & [Location]` (Using a pipe `|` as a separator; choose one unlikely to be in your actual data). Click OK.
    2.  **Count Occurrences of the Key:** We need to count how many times each unique `RiskLocationKey` appears in the dataset *across different time periods*.
        *   Right-click the header of the `RiskLocationKey` column -> 'Group By'.
        *   Keep 'Basic' selected.
        *   Group by: `RiskLocationKey`.
        *   New column name: `RiskLocationOccurrences`
        *   Operation: 'Count Rows'.
        *   Click OK. *This creates a new, temporary table showing each unique key and its total count.* Let's assume this new query/step is named "Grouped Rows".
    3.  **Merge Counts back to Original Data:** Now, join this count back to your main data table.
        *   Go back to your main query/previous step (before the grouping).
        *   Go to the 'Home' tab -> 'Merge Queries' (choose 'Merge Queries' to modify the current table, or 'Merge Queries as New' if preferred).
        *   In the Merge dialog:
            *   Select `RiskLocationKey` in the top (current) table.
            *   Select the "Grouped Rows" query/table in the dropdown for the bottom table.
            *   Select `RiskLocationKey` in the bottom table.
            *   Join Kind: 'Left Outer (all from first, matching from second)'.
            *   Click OK.
    4.  **Expand Merged Data:** You'll see a new column, likely named after the grouped query (e.g., "Grouped Rows"), with 'Table' in each cell. Click the expand icon ( wygląda ) in the column header.
        *   Deselect 'RiskLocationKey' (we already have it).
        *   Make sure `RiskLocationOccurrences` is selected.
        *   *Uncheck* 'Use original column name as prefix'.
        *   Click OK. You now have the `RiskLocationOccurrences` count on each row.
    5.  **Create Repeat Flag:** Add a conditional column based on the count.
        *   Go to 'Add Column' -> 'Conditional Column'.
        *   New column name: `Is Repeat Finding`
        *   Rule: If `RiskLocationOccurrences` -> `is greater than` -> `1`
        *   Then Output: `Yes`
        *   Else Output: `No`
        *   Click OK.
    6.  **(Optional Cleanup):** You can now remove the `RiskLocationKey` and `RiskLocationOccurrences` columns if you only need the final `Is Repeat Finding` flag. Right-click their headers -> 'Remove'.
*   **Insight Enabled:**
    *   You can now filter visuals specifically for `Is Repeat Finding = Yes`.
    *   Create charts showing the trend of repeat findings over time (`QuarterStartDate` on Axis, `Risk Count` on Values, filtered for `Is Repeat Finding = Yes`). Is the number of repeat issues increasing or decreasing?
    *   Identify which `L3risks` and `Locations` have the most repeat findings using bar charts or matrices. This directly points to areas needing focused management attention and root cause analysis.

**Calculation 7: Risk Density per Review Instance**

*   **Purpose:** To understand how many risks are typically identified *within a single review instance*. A review instance might be defined by the `Review_Name`, `Quarter`, and perhaps the `LOD Team`. This helps contextualize the number of findings – finding 2 risks might be normal for one review type but exceptional for another.
*   **Method (Power Query):**
    1.  **Create a Unique Key for Review Instance:**
        *   Go to 'Add Column' -> 'Custom Column'.
        *   New column name: `ReviewInstanceKey`
        *   Formula: `[Review_Name] & "|" & [Quarter] & "|" & [LOD Team]` (Adjust if your definition of a unique review instance is different). Click OK.
    2.  **Count Risks within each Instance:** Group by this key to count risks per instance.
        *   Right-click the header of the `ReviewInstanceKey` column -> 'Group By'.
        *   Group by: `ReviewInstanceKey`.
        *   New column name: `RisksPerReviewInstance`
        *   Operation: 'Sum'.
        *   Column: `Risk Count` (the column of 1s we created earlier).
        *   Click OK. This again creates a temporary grouped table. Let's call this "Grouped Reviews".
    3.  **Merge Counts back to Original Data:**
        *   Go back to your main query/step before grouping.
        *   Go to 'Home' tab -> 'Merge Queries'.
        *   Select `ReviewInstanceKey` in the top table.
        *   Select the "Grouped Reviews" query/table below.
        *   Select `ReviewInstanceKey` in the bottom table.
        *   Join Kind: 'Left Outer'.
        *   Click OK.
    4.  **Expand Merged Data:** Click the expand icon on the new merged column header.
        *   Deselect `ReviewInstanceKey`.
        *   Ensure `RisksPerReviewInstance` is selected.
        *   Uncheck 'Use original column name as prefix'.
        *   Click OK.
    5.  **(Optional Cleanup):** Remove the `ReviewInstanceKey` column if desired.
*   **Insight Enabled:**
    *   **Analyze Review Effectiveness/Scope:** Create a histogram or box plot of `RisksPerReviewInstance`. What is the typical number of findings per review? Are there outliers (reviews finding exceptionally high or low numbers of risks)?
    *   **Compare Review Types:** Use a bar chart with `Review_Name` on the axis and *Average* of `RisksPerReviewInstance` on the values. Which types of reviews consistently yield more findings? Does this reflect the inherent risk of the area reviewed or the thoroughness of the review process?
    *   **Contextualize Individual Risks:** While maybe less direct in a visual, knowing a specific risk was 1 of 2 found vs. 1 of 20 found in its respective review provides important context during investigation.

**Applying in Power BI:**

*   **Repeat Risks:**
    *   Use a Slicer on `Is Repeat Finding`.
    *   Create a stacked bar chart: Axis = `QuarterStartDate`, Legend = `Is Repeat Finding`, Values = `Count of Risk Count`. This shows the proportion of new vs. repeat risks over time.
    *   Create a table/matrix filtered for `Is Repeat Finding = Yes`, showing `L3risks`, `Location`, and `Count of Risk Count` to list the top recurring issues.
*   **Risk Density:**
    *   Create a bar chart: Axis = `Review_Name`, Values = `Average of RisksPerReviewInstance`. Add `Count of ReviewInstanceKey` (requires making the key distinct first or using distinct count in visual) to tooltips to see how many reviews contributed to the average.
    *   Use `RisksPerReviewInstance` in scatter plots, perhaps against another metric, to see if reviews finding more risks correlate with other factors.

These calculations add layers of context (repeatability, density) beyond simple counts and distributions, enabling more targeted analysis and action within a risk management framework.