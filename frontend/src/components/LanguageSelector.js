import { useTranslation } from "react-i18next";

const languages = [
  { code: "en", label: "🇬🇧" },
  { code: "pl", label: "🇵🇱" },
  { code: "ru", label: "🇷🇺" },
  { code: "ua", label: "🇺🇦" }
];

export default function LanguageSelector() {
  const { i18n } = useTranslation();

  return (
    <div className="flex gap-2 justify-end mb-4">
      {languages.map((lang) => (
        <button
          key={lang.code}
          onClick={() => i18n.changeLanguage(lang.code)}
          className={`text-2xl ${i18n.language === lang.code ? "opacity-100" : "opacity-50"} hover:opacity-100 transition`}
        >
          {lang.label}
        </button>
      ))}
    </div>
  );
}
