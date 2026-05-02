import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Commercial Bank Trading Analysis",
    layout="wide"
)

# LOAD DATA
@st.cache_data
def load_data():
    return pd.read_excel("data/annual_trading_statistics.xlsx")

df = load_data()

# Filter Commercial Bank shares
comb = df[df["Symbol"].isin(["COMB.N0000", "COMB.X0000"])].copy()

# Create volatility variable
comb["Volatility"] = comb["High_(Rs)"] - comb["Low_(Rs)"]

# Sort data
comb = comb.sort_values(["Symbol", "Year"])

# Create Turnover Growth
comb["Turnover_Growth_%"] = (
    comb.groupby("Symbol")["Turnover(Rs)"]
    .pct_change() * 100
)

# PHASE ASSIGNMENT
def assign_phase(row):

    # Voting shares phases
    if row["Symbol"] == "COMB.N0000":
        if row["Year"] < 2013:
            return "Phase 1: Growth"
        elif row["Year"] < 2020:
            return "Phase 2: Decline"
        else:
            return "Phase 3: Expansion"

    # Non-voting shares phases
    elif row["Symbol"] == "COMB.X0000":
        if row["Year"] < 2014:
            return "Phase 1: Growth"
        elif row["Year"] < 2020:
            return "Phase 2: Decline"
        else:
            return "Phase 3: Expansion"

# PAGE NAVIGATION
if "page" not in st.session_state:
    st.session_state.page = "Introduction"

page = st.sidebar.radio(
    "Select Section",
    ["Introduction", "Data & Visualisation", "Market Analysis"],
    index=["Introduction", "Data & Visualisation", "Market Analysis"].index(st.session_state.page)
)

st.session_state.page = page


if page == "Introduction":

    # Center the logo
    col1, col2, col3 = st.columns([3,2,3])
    with col2:
        st.image("assets/cmb.png", width=200)

    # Title
    st.markdown(
        """
        <h1 style='text-align: center;'>Commercial Bank of Ceylon PLC</h1>
        <h3 style='text-align: center;'>Stock Market Trading Analysis</h3>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # ABOUT COMPANY
    st.subheader("About the Company")

    st.write(
        """
        Commercial Bank of Ceylon PLC is one of the largest private sector banks in Sri Lanka.
        The bank's shares are actively traded on the Colombo Stock Exchange (CSE), providing
        investors with opportunities to participate in the bank's ownership and financial
        performance.
        """
    )

    # SHARE CLASSES
    st.subheader("Share Classes")

    st.markdown(
        """
        Commercial Bank shares are listed in two classes:

        **Voting Shares (COMB.N0000)**  
        - Provide shareholders with voting rights in corporate decisions  
        - Investors can vote on matters such as electing directors and major policy decisions  

        **Non-Voting Shares (COMB.X0000)**  
        - Do not provide voting rights  
        - Investors still receive dividends and benefit from share price changes  

        Both share classes may display different trading patterns, which makes it useful
        to analyse them separately.
        """
    )

    st.divider()

    st.subheader("Dashboard Guide")

    # DATA VISUALISATION SECTION
    col1, col2 = st.columns([4,1])

    with col1:
        st.markdown(
        """
        **Data & Visualisation**

        Explore trading statistics of Commercial Bank shares, including turnover trends,
        price volatility, and turnover growth over time. Users can filter by share class
        and year range to interactively examine the trading behaviour.
        """
        )

    with col2:
        if st.button("Open", key="data_page"):
            st.session_state.page = "Data & Visualisation"
            st.rerun()

    st.write("")

    # MARKET ANALYSIS SECTION
    col3, col4 = st.columns([4,1])

    with col3:
        st.markdown(
        """
        **Market Analysis**

        Investigate statistical relationships between turnover and market indicators using
        robust regression models. The section also examines whether turnover in the current
        year is influenced by trading activity in the previous year.
        """
        )

    with col4:
        if st.button("Open", key="analysis_page"):
            st.session_state.page = "Market Analysis"
            st.rerun()

    st.divider()

    col1, col2 = st.columns([3,3])
    with col1:
        st.subheader("Key Variables Used")
    
        st.markdown("""
        - **Turnover** – Total value of shares traded  
        - **Share Volume** – Number of shares traded  
        - **Trade Volume** – Number of trades executed  
        - **Volatility (High–Low Range)** – Price fluctuation within a year  
        - **Market Phases** – Growth, Decline, and Expansion periods
        """)
    with col2:
        st.image("assets/chart.png", width=700)

# DATA & VISUALISATION PAGE
if page == "Data & Visualisation":
    st.markdown("""
    <style>
    
    /* Make only metric labels green */
    [data-testid="stMetricLabel"] {
        color: #00C46A;
        font-weight: 600;
    }
    
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.header("Filter Options")

    share_type = st.sidebar.selectbox(
        "Select Share Class",
        ["Both", "COMB.N0000", "COMB.X0000"]
    )

    year_range = st.sidebar.slider(
        "Select Year Range",
        int(comb["Year"].min()),
        int(comb["Year"].max()),
        (2006, 2022)
    )

    # Apply filters
    filtered = comb[
        (comb["Year"] >= year_range[0]) &
        (comb["Year"] <= year_range[1])
    ]

    # SUMMARY STATISTICS
    if share_type != "Both":
        filtered = filtered[filtered["Symbol"] == share_type]

    filtered["Phase"] = filtered.apply(assign_phase, axis=1)

    share_map = {
        "COMB.N0000": "Voting Shares (COMB.N0000)",
        "COMB.X0000": "Non-Voting Shares (COMB.X0000)",
        "Both": "Voting and Non-Voting Shares"
    }

    share_name = share_map[share_type]

    # MAIN TITLE
    st.markdown(
    f"""
    <h1 style='text-align: center;'>Trading Analysis — {share_name}</h1>
    """,
    unsafe_allow_html=True
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average Turnover",
        f"{filtered['Turnover(Rs)'].mean():,.0f}"
    )

    col2.metric(
        "Average Volatility",
        f"{filtered['Volatility'].mean():.2f}"
    )

    col3.metric(
        "Total Trades",
        f"{filtered['Trade_Volume'].sum():,.0f}"
    )

    st.divider()

    # TURNOVER WITH PHASE SHADING
    st.header("Turnover Over Time")

    col1, col2 = st.columns([4,1])

    with col1:

        fig1 = px.line(
            filtered,
            x="Year",
            y="Turnover(Rs)",
            color="Symbol",
            markers=True,
            title=f"Annual Turnover — {share_name}"
        )

        phase_colors = {
            "Phase 1: Growth": "rgba(0,255,150,0.30)",
            "Phase 2: Decline": "rgba(255,80,80,0.35)",
            "Phase 3: Expansion": "rgba(80,160,255,0.35)"
        }

        if share_type != "Both":
            for phase, color in phase_colors.items():

                phase_data = filtered[filtered["Phase"] == phase]

                if not phase_data.empty:
                    fig1.add_vrect(
                        x0=phase_data["Year"].min(),
                        x1=phase_data["Year"].max(),
                        fillcolor=color,
                        opacity=1,
                        line_width=2,
                        line_color="white",
                        annotation_text=phase,
                        annotation_position="top left"
                    )

        fig1.update_layout(
            plot_bgcolor="#0E1117",
            paper_bgcolor="#0E1117"
        )

        st.plotly_chart(fig1, use_container_width=True)

    with col2:

        if share_type == "Both":
            st.info(
            """
            Voting shares (COMB.N0000) consistently exhibit higher turnover than
            non-voting shares (COMB.X0000) throughout the observed period,
            indicating stronger trading activity and investor preference for
            shares with voting rights.
            """
            )

        elif share_type == "COMB.N0000":
            st.info(
            """
            Voting shares show relatively high trading activity over time.
            Turnover increased during the early years, declined in the mid-period,
            and expanded again in recent years.
            """
            )
    
        elif share_type == "COMB.X0000":
            st.info(
            """
            Non-voting shares experience lower turnover compared to voting shares.
            The trading pattern shows early growth, followed by a decline,
            and a sharp recovery in the most recent year.
            """
            )
    
        max_year = filtered.loc[
            filtered["Turnover(Rs)"].idxmax(),
            "Year"
        ]

        st.success(f"Highest turnover occurred in {max_year}.")
        
    st.divider()

    # TURNOVER GROWTH
    st.header("Year-over-Year Turnover Growth (%)")

    latest_growth = filtered["Turnover_Growth_%"].iloc[-1]

    col1, col2 = st.columns([1,4])

    with col1:

        if share_type != "Both":
    
            st.metric(
                label="Latest Growth",
                value=f"{latest_growth:.2f}%",
                delta=f"{latest_growth:.2f}%"
            )
    
            if share_type == "COMB.N0000":
                st.info(
                """
                Voting shares display notable fluctuations in turnover growth,
                reflecting periods of expansion, contraction, and a strong
                recovery in the most recent year.
                """
                )
    
            elif share_type == "COMB.X0000":
                st.info(
                """
                Non-voting shares exhibit more volatile growth patterns,
                with sharp declines followed by a strong rebound in the
                the latest year.
                """
                )
    
        else:
    
            st.info(
            """
            The chart compares turnover growth rates for both voting and
            non-voting shares. Growth patterns generally follow similar
            market cycles, though voting shares tend to experience larger
            trading expansions.
            """
            )

    with col2:

        fig4 = px.bar(
            filtered,
            x="Year",
            y="Turnover_Growth_%",
            color="Symbol",
            barmode="group",
            title="Annual Turnover Growth Rate",
            hover_data=["Turnover(Rs)"]
        )

        fig4.update_layout(
            yaxis_title="Growth Rate (%)",
            plot_bgcolor="#0E1117",
            paper_bgcolor="#0E1117"
        )

        st.plotly_chart(fig4, use_container_width=True)

    st.divider()

    # VOLATILITY
    st.header("Price Volatility Over Time")
    
    col1, col2 = st.columns([4,1])
    
    with col1:
    
        fig2 = px.line(
            filtered,
            x="Year",
            y="Volatility",
            color="Symbol",
            markers=True
        )
    
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
    
        if share_type == "Both":
            st.info(
            """
            This chart compares price volatility trends of voting and non-voting shares over time.
            Voting shares generally exhibit higher volatility, indicating stronger price fluctuations
            and greater sensitivity to market conditions. Both share classes follow similar cyclical
            patterns, suggesting they are influenced by common market forces.
            """
            )
    
        elif share_type == "COMB.N0000":
            st.info(
            """
            Voting shares display relatively high volatility, with noticeable spikes in earlier years
            followed by gradual stabilization. This indicates stronger investor activity but also
            higher exposure to price fluctuations during uncertain periods.
            """
            )
    
        elif share_type == "COMB.X0000":
            st.info(
            """
            Non-voting shares show comparatively lower volatility, reflecting more stable price
            movements over time. Fluctuations are less extreme, suggesting a more conservative
            trading behavior.
            """
            )
    
        # Optional dynamic insight
        max_vol_year = filtered.loc[
            filtered["Volatility"].idxmax(),
            "Year"
        ]
    
        st.success(f"Highest volatility occurred in {max_vol_year}.")
        
    st.divider()
    
    # VARIABLE RELATIONSHIPS
    st.header("Explore Variable Relationships")

    x_var = st.selectbox(
        "Select X Variable",
        ["Volatility", "Share_Volume", "Trade_Volume"]
    )
    
    y_var = st.selectbox(
        "Select Y Variable",
        ["Turnover(Rs)", "Volatility"]
    )

    col1, col2 = st.columns([4,1])

    with col1:
        show_trend = st.checkbox(
        "Show Regression Trendline",
        value=True
        )

        trend = "ols" if show_trend else None

        fig3 = px.scatter(
            filtered,
            x=x_var,
            y=y_var,
            color="Symbol",
            size="Share_Volume",
            trendline=trend,
            hover_data=["Year"]
        )

        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        if share_type == "Both":

            if x_var == "Volatility" and y_var == "Turnover(Rs)":
                st.info(
                """
                This plot explores how price volatility relates to turnover for both share classes.
                A positive relationship suggests that higher price fluctuations are associated with
                increased trading activity. Voting shares tend to show stronger turnover responses
                to volatility compared to non-voting shares.
                """
                )
        
            elif x_var == "Share_Volume" and y_var == "Turnover(Rs)":
                st.info(
                """
                This plot shows the relationship between share volume and turnover.
                A strong positive association is expected, as higher traded quantities typically
                lead to higher total transaction values. Differences between share classes reflect
                varying investor participation levels.
                """
                )
        
            elif x_var == "Trade_Volume" and y_var == "Turnover(Rs)":
                st.info(
                """
                This visualization examines how the number of trades relates to turnover.
                An upward trend indicates that increased trading frequency contributes to
                a higher overall market value exchanged.
                """
                )
        
            elif y_var == "Volatility":
                st.info(
                """
                This plot highlights factors influencing price volatility across both share classes.
                Variations suggest that trading activity and volume may impact price stability,
                with voting shares generally showing stronger sensitivity.
                """
                )
        
        elif share_type == "COMB.N0000":
        
            if x_var == "Volatility" and y_var == "Turnover(Rs)":
                st.info(
                """
                For voting shares, higher volatility is generally associated with increased turnover,
                indicating that price fluctuations encourage active trading and investor participation.
                """
                )
        
            elif x_var == "Share_Volume" and y_var == "Turnover(Rs)":
                st.info(
                """
                Turnover increases strongly with share volume, confirming that higher quantities traded
                drive overall market value for voting shares.
                """
                )
        
            elif x_var == "Trade_Volume" and y_var == "Turnover(Rs)":
                st.info(
                """
                A positive relationship between trade volume and turnover suggests that frequent trading
                activity contributes significantly to market liquidity in voting shares.
                """
                )
        
            elif y_var == "Volatility":
                st.info(
                """
                Voting share volatility appears sensitive to trading activity, with higher volumes often
                corresponding to greater price fluctuations.
                """
                )
        
        elif share_type == "COMB.X0000":
        
            if x_var == "Volatility" and y_var == "Turnover(Rs)":
                st.info(
                """
                Non-voting shares show a weaker relationship between volatility and turnover,
                suggesting that price fluctuations have a smaller impact on trading activity.
                """
                )
        
            elif x_var == "Share_Volume" and y_var == "Turnover(Rs)":
                st.info(
                """
                Turnover increases with share volume, though the relationship is less pronounced
                compared to voting shares, indicating relatively lower trading intensity.
                """
                )
        
            elif x_var == "Trade_Volume" and y_var == "Turnover(Rs)":
                st.info(
                """
                Trade frequency contributes to turnover, but the effect is more moderate,
                reflecting more stable and less aggressive trading behavior.
                """
                )
        
            elif y_var == "Volatility":
                st.info(
                """
                Volatility in non-voting shares remains relatively stable, with weaker sensitivity
                to changes in trading activity and volume.
                """
                )

        corr = filtered[[x_var, y_var]].corr().iloc[0,1]

        # Determine strength
        relationship_strength = (
            "Strong" if abs(corr) > 0.7 else
            "Moderate" if abs(corr) > 0.4 else
            "Weak"
        )
    
        st.success(
            f"Correlation between {x_var} and {y_var}: {corr:.2f} "
            f" - {relationship_strength} relationship"
        )
        
        st.caption("Bubble size represents share trading volume.")

    st.divider()

    # DATA TABLE
    st.header("Annual Trading Statistics")
    st.dataframe(filtered)

# MARKET ANALYSIS
if page == "Market Analysis":

    st.sidebar.header("Filter Options")

    share_type = st.sidebar.selectbox(
        "Select Share Class",
        ["COMB.N0000", "COMB.X0000"]
    )

    import statsmodels.api as sm
    from statsmodels.robust.robust_linear_model import RLM
    from statsmodels.robust.norms import HuberT

    # CENTERED TITLE
    st.markdown(
        f"<h1 style='text-align: center;'>Relationship between Market Indicators — {share_type}</h1>",
        unsafe_allow_html=True
    )

    st.divider()

    model_data = comb.copy()

    # Apply share class filter
    model_data = model_data[model_data["Symbol"] == share_type]

    model_data["Phase"] = model_data.apply(assign_phase, axis=1)

    model_data["log_turnover"] = np.log(model_data["Turnover(Rs)"])
    model_data = model_data.dropna()

    # Dummy variables
    phase_dummies = pd.get_dummies(
        model_data["Phase"],
        drop_first=True
    ).astype(float)

    X = pd.concat([
        model_data[["Volatility", "Share_Volume", "Trade_Volume"]],
        phase_dummies
    ], axis=1)

    y = model_data["log_turnover"]
    X = sm.add_constant(X)

    # ROBUST MODEL
    robust_model = RLM(y, X, M=HuberT()).fit()

    st.header("Robust Linear Model")
    st.subheader("Results")

    results_table = pd.DataFrame({
        "Variable": X.columns,
        "Coefficient": robust_model.params,
        "Std Error": robust_model.bse,
        "z-value": robust_model.tvalues,
        "P-value": robust_model.pvalues,
        "CI Lower": robust_model.conf_int()[0],
        "CI Upper": robust_model.conf_int()[1]
    }).round(4)

    col1, col2 = st.columns([4,1])

    with col1:
        st.dataframe(results_table, use_container_width=True, hide_index=True)

    with col2:
        st.info(
            """
            Robust Linear Model (RLM) is used to estimate the relationship
            between turnover and market indicators while reducing the
            influence of outliers.
            """
        )

     # SIMPLE INTERPRETATION
    st.subheader("Impact of Market Indicators on Turnover")

    coef_df = pd.DataFrame({
        "Variable": robust_model.params.index,
        "Coefficient": robust_model.params.values
    })
    
    coef_df = coef_df[coef_df["Variable"] != "const"]
    
    # Chart + Insights
    col1, col2 = st.columns([3,2])
    
    with col1:
        fig_coef = px.bar(
            coef_df,
            x="Variable",
            y="Coefficient",
            title="Effect of Each Variable on Turnover",
            height=350
        )

        fig_coef.update_layout(title_x=0.3, title_font=dict(size=20))
        
        st.plotly_chart(fig_coef, use_container_width=True)
    
    with col2:
        st.subheader("Key Insights")
    
        significant_vars = results_table[results_table["P-value"] < 0.05]["Variable"].tolist()
    
        if len(significant_vars) == 0:
            st.info("No variables show a statistically strong relationship with turnover.")
        else:
            readable_vars = [v.replace("_", " ") for v in significant_vars if v != "const"]
    
            st.success(
                f"The model suggests that **{', '.join(readable_vars)}** significantly influence trading turnover."
            )
    
        st.caption("Significance level: p-value < 0.05")
        
    # MODEL EQUATION
    st.header("Estimated Regression Model")

    params = robust_model.params

    st.latex(
    rf"""
    \begin{{aligned}}
    \log(Turnover) &= {params['const']:.4f} \\
    &+ {params['Volatility']:.4f}(High\!-\!Low\ Range) \\
    &+ {params['Share_Volume']:.2e}(Share\ Volume) \\
    &+ {params['Trade_Volume']:.2e}(Trade\ Volume) \\
    &+ {params.get('Phase 2: Decline',0):.4f}(Phase\ 2:\ Decline) \\
    &+ {params.get('Phase 3: Expansion',0):.4f}(Phase\ 3:\ Expansion) \\
    &+ \epsilon
    \end{{aligned}}
    """
    )

    st.info(
    """
    This model estimates how different market indicators influence trading turnover.
    Positive coefficients suggest that increases in these indicators
    are associated with higher trading turnover.
    """
    )

    with st.expander("Assumptions & Limitations"):

        st.markdown("""
            ### Assumptions
            - The relationship between market indicators and turnover is linear.
            - Observations are independent of each other.
            - Independent variables are not perfectly correlated (no multicollinearity).
        
            ### Limitations
            - Although robust to outliers, extreme values may still influence results.
            - The model only captures linear relationships and may miss complex patterns.
            - Coefficients may be less efficient if the data has no significant outliers.
            - Market phases are simplified into discrete categories, which may not fully reflect real market behavior.
            """)

    # Create lagged turnover variable
    model_data = model_data.sort_values("Year")
    
    model_data["lag_log_turnover"] = model_data["log_turnover"].shift(1)
    
    lag_data = model_data.dropna(subset=["lag_log_turnover", "log_turnover"])

    if lag_data.empty:
        st.warning("Not enough data available to perform lag analysis.")
        st.stop()

    st.divider()

    st.header("Turnover Persistence Analysis")

    st.write(
    """
    This analysis examines whether trading activity in the current year
    is influenced by trading activity in the previous year.
    """
    )

    st.subheader("Lag Regression Model")

    X_lag = sm.add_constant(lag_data["lag_log_turnover"])
    y_lag = lag_data["log_turnover"]
    
    lag_model = sm.OLS(y_lag, X_lag).fit()

    col1, col2, col3 = st.columns(3)

    def styled_metric(label, value):
        st.markdown(
            f"""
            <div style="
                background-color:#111827;
                padding:10px;
                border-radius:8px;
                text-align:center;
                border:1px solid #2d3748;
            ">
                <div style="font-size:13px; color:#9ca3af;">{label}</div>
                <div style="font-size:20px; font-weight:bold;">{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    coef = lag_model.params["lag_log_turnover"]
    pval = lag_model.pvalues["lag_log_turnover"]
    r2 = lag_model.rsquared
    
    with col1:
        styled_metric("Persistence Coefficient", f"{coef:.3f}")
    
    with col2:
        styled_metric("P-value", f"{pval:.4f}")
    
    with col3:
        styled_metric("R²", f"{r2:.3f}")

    st.markdown("<br>", unsafe_allow_html=True)
    
    lag_table = pd.DataFrame({
    "Variable": lag_model.params.index,
    "Coefficient": lag_model.params.values,
    "Std Error": lag_model.bse.values,
    "t-value": lag_model.tvalues.values,
    "P-value": lag_model.pvalues.values
    }).round(4)

    st.dataframe(lag_table, use_container_width=True, hide_index=True)

    params = lag_model.params

    st.latex(
    rf"""
    \log(Turnover_t) =
    {params['const']:.4f}
    +
    {params['lag_log_turnover']:.4f}\log(Turnover_{{t-1}})
    +
    \epsilon_t
    """
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([4,1])
    
    with col1:

        fig_lag = px.scatter(
            lag_data,
            x="lag_log_turnover",
            y="log_turnover",
            trendline="ols",
            title="Current vs Previous Year Turnover",
            labels={
                "lag_log_turnover": "Previous Year log(Turnover)",
                "log_turnover": "Current Year log(Turnover)"
            }
        )
        
        fig_lag.update_traces(
            marker=dict(size=8, opacity=0.7)
        )
        
        fig_lag.update_layout(
            height=400,
            title_x=0.3,
            title_font=dict(size=20)
        )
    
        st.plotly_chart(fig_lag, use_container_width=True)

    with col2:

        if coef > 0.7:
            strength = "strong"
        elif coef > 0.4:
            strength = "moderate"
        else:
            strength = "weak"
        
        st.info(
            f"""
            The relationship between past and current turnover is **{strength}**.
        
            A 1% increase in last year's turnover is associated with an approximate
            **{coef:.2f}% change** in current turnover.
            """
            )
        
    st.success(
       f"""
        {'This persistence is statistically significant, indicating that current trading turnover is significantly influenced by its previous values.' 
        if pval < 0.05 
        else 'The relationship is not statistically significant, suggesting that current trading turnover is not strongly influenced by its past values and may be driven by other market factors.'}
        """
    )

    with st.expander("Assumptions & Limitations"):

        st.markdown("""
            ### Assumptions
            - Current turnover is linearly related to the previous year's turnover.
            - Errors are uncorrelated and have constant variance (homoscedasticity).
        
            ### Limitations
            - Only one lag is considered, so longer-term dependencies are ignored.
            - The model assumes a constant relationship over time.
            - External market shocks and structural changes are not captured.
            - Small sample sizes may reduce the reliability of the estimates.
            """)