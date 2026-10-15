import io
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Калькулятор особистого бюджету — квартальний звіт",
    page_icon="📊",
    layout="wide",
)

CATEGORIES = [
    "Їжа",
    "Транспорт",
    "Розваги",
    "Житло / Комунальні",
    "Інше",
]

MONTH_NAMES = ["Місяць 1", "Місяць 2", "Місяць 3"]


def init_session_state() -> None:
    """Ініціалізує стан застосунку."""
    if "monthly_results" not in st.session_state:
        st.session_state.monthly_results = {
            month: None for month in MONTH_NAMES
        }


def calculate_month_budget(
    income: float, expenses: dict
) -> tuple[pd.DataFrame, float, float, str]:
    """Розраховує бюджет за місяць.

    Returns:
        df: DataFrame з витратами
        total_expenses: загальна сума витрат
        balance: залишок коштів
        status: статус бюджету
    """
    data = []
    for cat in CATEGORIES:
        amount = expenses.get(cat, 0.0)
        data.append({"Категорія": cat, "Сума": amount})

    df = pd.DataFrame(data)
    total_expenses = float(df["Сума"].sum())
    balance = income - total_expenses

    if balance > 0:
        status = "Профіцитний бюджет ✅"
    elif balance < 0:
        status = "Дефіцитний бюджет ⚠️"
    else:
        status = "Збалансований бюджет ⚖️"

    return df, total_expenses, balance, status


def save_month_result(
    month_name: str,
    income: float,
    df: pd.DataFrame,
    total_expenses: float,
    balance: float,
    status: str,
) -> None:
    """Зберігає результат місяця в session_state."""
    month_df = df.copy()
    month_df["Місяць"] = month_name

    st.session_state.monthly_results[month_name] = {
        "income": income,
        "expenses_df": month_df,
        "total_expenses": total_expenses,
        "balance": balance,
        "status": status,
    }


def render_month_tab(month_name: str) -> None:
    """Відображає вкладку одного місяця."""
    st.subheader(f"Введення даних для: {month_name}")

    saved_data = st.session_state.monthly_results.get(month_name)
    default_income = saved_data["income"] if saved_data else 30000.0

    income = st.number_input(
        f"Дохід за {month_name} (грн)",
        min_value=0.0,
        value=default_income,
        step=1000.0,
        key=f"income_{month_name}",
    )

    st.markdown("### Витрати по категоріях")
    expenses = {}
    
    # Використовуємо дві колонки для зручнішого введення
    cols = st.columns(2)
    for i, cat in enumerate(CATEGORIES):
        default_val = 0.0
        if saved_data and not saved_data["expenses_df"].empty:
            match_row = saved_data["expenses_df"][
                saved_data["expenses_df"]["Категорія"] == cat
            ]
            if not match_row.empty:
                default_val = float(match_row["Сума"].values[0])

        col_idx = i % 2
        with cols[col_idx]:
            expenses[cat] = st.number_input(
                f"{cat} (грн)",
                min_value=0.0,
                value=default_val,
                step=500.0,
                key=f"exp_{month_name}_{cat}",
            )

    if st.button(f"Розрахувати та зберегти {month_name}", key=f"btn_{month_name}"):
        df, total_expenses, balance, status = calculate_month_budget(income, expenses)
        save_month_result(month_name, income, df, total_expenses, balance, status)
        st.success(f"Дані для {month_name} успішно збережено!")

    # Відображення поточних результатів для місяця, якщо вони є
    if st.session_state.monthly_results.get(month_name) is not None:
        res = st.session_state.monthly_results[month_name]
        st.markdown("---")
        st.markdown(f"### Результати за {month_name}")
        
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("Загальний дохід", f"{res['income']:,.2f} грн")
        m_col2.metric("Загальні витрати", f"{res['total_expenses']:,.2f} грн", delta_color="inverse")
        m_col3.metric("Залишок", f"{res['balance']:,.2f} грн", delta=res['status'])

        st.dataframe(res["expenses_df"][["Категорія", "Сума"]], use_container_width=True)


def build_quarterly_expenses_df() -> pd.DataFrame:
    """Об'єднує витрати за всі місяці в один DataFrame."""
    all_dfs = []
    for month_name in MONTH_NAMES:
        data = st.session_state.monthly_results.get(month_name)
        if data and "expenses_df" in data:
            all_dfs.append(data["expenses_df"])

    if not all_dfs:
        return pd.DataFrame(columns=["Місяць", "Категорія", "Сума"])

    combined_df = pd.concat(all_dfs, ignore_index=True)
    return combined_df[["Місяць", "Категорія", "Сума"]]


def build_quarterly_summary_df(combined_df: pd.DataFrame) -> pd.DataFrame:
    """Створює зведення витрат по категоріях."""
    if combined_df.empty:
        return pd.DataFrame(columns=["Категорія", "Сума"])
    
    summary_df = (
        combined_df.groupby("Категорія")["Сума"]
        .sum()
        .reset_index()
        .sort_values(by="Сума", ascending=False)
    )
    return summary_df

def build_export_csv() -> bytes:
    """Формує CSV-файл квартального звіту."""
    rows = []
    total_income = 0.0
    total_expenses = 0.0

    for month_name in MONTH_NAMES:
        data = st.session_state.monthly_results.get(month_name)
        if data:
            total_income += data["income"]
            total_expenses += data["total_expenses"]
            
            # Додаємо рядки витрат по місяцях
            for _, row in data["expenses_df"].iterrows():
                rows.append({
                    "Місяць": month_name,
                    "Категорія": row["Категорія"],
                    "Сума": row["Сума"],
                })

    total_balance = total_income - total_expenses

    # Додаємо підсумкові рядки для кварталу з міткою "ВСЬОГО"
    rows.append({"Місяць": "ВСЬОГО", "Категорія": "ДОХІД", "Сума": total_income})
    rows.append({"Місяць": "ВСЬОГО", "Категорія": "ВИТРАТИ", "Сума": total_expenses})
    rows.append({"Місяць": "ВСЬОГО", "Категорія": "БАЛАНС", "Сума": total_balance})

    export_df = pd.DataFrame(rows)
    if export_df.empty:
        export_df = pd.DataFrame(columns=["Місяць", "Категорія", "Сума"])

    csv_buffer = io.StringIO()
    export_df.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
    return csv_buffer.getvalue().encode("utf-8-sig")


def render_quarter_report() -> None:
    """Відображає квартальний звіт."""
    st.header("📈 Зведений квартальний звіт")

    # Перевіримо, чи заповнено хоча б один місяць
    completed_months = [
        m for m in MONTH_NAMES if st.session_state.monthly_results.get(m) is not None
    ]

    if not completed_months:
        st.warning("Будь ласка, заповніть та збережіть дані хоча б за один місяць у вкладці «Місячні дані».")
        return

    # Загальні показники за квартал
    total_quarter_income = sum(
        st.session_state.monthly_results[m]["income"] for m in completed_months
    )
    total_quarter_expenses = sum(
        st.session_state.monthly_results[m]["total_expenses"] for m in completed_months
    )
    total_quarter_balance = total_quarter_income - total_quarter_expenses

    q_col1, q_col2, q_col3 = st.columns(3)
    q_col1.metric("Сумарний дохід", f"{total_quarter_income:,.2f} грн")
    q_col2.metric("Сумарні витрати", f"{total_quarter_expenses:,.2f} грн")
    q_col3.metric("Загальний баланс", f"{total_quarter_balance:,.2f} грн")

    st.markdown("---")

    combined_df = build_quarterly_expenses_df()
    
    col_l, col_r = st.columns(2)
    
    with col_l:
        st.subheader("Зведення витрат по категоріях за квартал")
        summary_df = build_quarterly_summary_df(combined_df)
        st.dataframe(summary_df, use_container_width=True)

    with col_r:
        st.subheader("Розподіл витрат")
        if not summary_df.empty:
            st.bar_chart(summary_df.set_index("Категорія")["Сума"])

    st.markdown("---")
    st.subheader("Детальні дані по всіх місяцях")
    st.dataframe(combined_df, use_container_width=True)

    # Кнопка для завантаження CSV
    csv_data = build_export_csv()
    st.download_button(
        label="📥 Завантажити квартальний звіт у форматі CSV",
        data=csv_data,
        file_name="quarterly_budget_report.csv",
        mime="text/csv",
    )


def main() -> None:
    init_session_state()

    st.title("💰 Калькулятор особистого бюджету — рівень 2")
    st.write(
        "Додаток дозволяє вести бюджет за 3 місяці та формувати зведений квартальний звіт."
    )

    section = st.sidebar.radio(
        "Навігація",
        ["Місячні дані", "Квартальний звіт"],
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Стан заповнення")
    for month_name in MONTH_NAMES:
        if st.session_state.monthly_results.get(month_name) is not None:
            st.sidebar.success(f"{month_name}: готово")
        else:
            st.sidebar.info(f"{month_name}: немає розрахунку")

    if section == "Місячні дані":
        st.header("📅 Дані по місяцях")
        tabs = st.tabs(MONTH_NAMES)

        for tab, month_name in zip(tabs, MONTH_NAMES):
            with tab:
                render_month_tab(month_name)

    elif section == "Квартальний звіт":
        render_quarter_report()


if __name__ == "__main__":
    main()