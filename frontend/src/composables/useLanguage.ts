import { ref, computed } from "vue";

const currentLanguage = ref("vi"); // Default to Vietnamese

const translations: Record<string, any> = {
  vi: {
    login: {
      goBack: "Trang chủ",
      title: "Đăng nhập",
      subtitle: "Vui lòng đăng nhập để tiếp tục",
      username: "Tên đăng nhập",
      password: "Mật khẩu",
      placeholder: {
        username: "Nhập tên đăng nhập",
        password: "Nhập mật khẩu",
      },
      button: "Đăng nhập",
      forgot: "Quên mật khẩu?",
      copyright: "Bản quyền thuộc về © 2025 MediCare Hospital. ",
      error: {
        userNotFound: "Tên đăng nhập không tồn tại",
        wrongPassword: "Mật khẩu không đúng",
        failedLogin:
          "Đăng nhập thất bại. Vui lòng kiểm tra thông tin đăng nhập.",
      },
    },
  },
  en: {
    login: {
      goBack: "Home",
      title: "Login",
      subtitle: "Please sign in to continue",
      username: "Username",
      password: "Password",
      placeholder: {
        username: "Enter username",
        password: "Enter password",
      },
      button: "Sign In",
      forgot: "Forgot password?",
      copyright: "© 2025 MediCare Hospital. All rights reserved.",
      error: {
        userNotFound: "Username does not exist",
        wrongPassword: "Incorrect password",
        failedLogin: "Login failed. Please check your login information.",
      },
    },
  },
};

export function useLanguage() {
  const t = (key: string) => {
    const keys = key.split(".");
    let value = translations[currentLanguage.value];

    for (const k of keys) {
      value = value?.[k];
    }

    return value || key;
  };

  const setLanguage = (lang: string) => {
    currentLanguage.value = lang;
  };

  const currentLang = computed(() => currentLanguage.value);

  return {
    t,
    setLanguage,
    currentLang,
  };
}
