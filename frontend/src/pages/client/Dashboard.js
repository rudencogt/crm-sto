// src/pages/client/Dashboard.js
import { useTranslation } from "react-i18next";
import SidebarLayout from "../../components/SidebarLayout";

export default function Dashboard() {
  const { t } = useTranslation();

  return (
    <SidebarLayout>
      <h1 className="text-2xl font-bold text-gray-800 mb-4">{t("dashboard.title")}</h1>
      <p className="text-gray-600">{t("dashboard.description")}</p>
    </SidebarLayout>
  );
}
