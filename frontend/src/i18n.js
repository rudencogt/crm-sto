import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import LanguageDetector from "i18next-browser-languagedetector";

import translationEn from "./locales/en/translation.json";
import translationPl from "./locales/pl/translation.json";
import translationRu from "./locales/ru/translation.json";
import translationUa from "./locales/ua/translation.json";

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources: {
      en: { translation: translationEn },
      pl: { translation: translationPl },
      ru: { translation: translationRu },
      ua: { translation: translationUa },
    },
    fallbackLng: "en",
    detection: {
      // 💡 вот это сохраняет язык в localStorage
      order: ["localStorage", "navigator"],
      caches: ["localStorage"],
    },
    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;
