const translations = {
  en: {
    lang: "Language",
    logout: "Logout",
    username: "Username",
    password: "Password",
    repeat_password: "Repeat password",
    remember: "Remember me",
    login_title: "Log in to your account",
    login_btn: "Log in",
    login_redirect: "Don't have an account yet?",
    login_redirect_url: "Create an account now!",
    signup_title: "Create a new account",
    signup_btn: "Sign up",
    signup_redirect: "Already have an account?",
    signup_redirect_url: "Log in then!",
    alert_bad_login: "Wrong login details",
    alert_username_in_use: "Username already in use",
    alert_password_mismatch: "Passwords do not match",
    notification_login_success: "You have logged in successfully!"
  },
  es: {
    lang: "Idioma",
    logout: "Cerrar sesión",
    username: "Usuario",
    password: "Contraseña",
    repeat_password: "Repetir contraseña",
    remember: "Recuérdame",
    login_title: "Inicia sesión en tu cuenta",
    login_btn: "Inicar sesión",
    login_redirect: "¿No tienes una cuenta todavía?",
    login_redirect_url: "Regístrate ahora!",
    signup_title: "Crea una nueva cuenta",
    signup_btn: "Registrarse",
    signup_redirect: "¿Ya tienes una cuenta?",
    signup_redirect_url: "Inicia sesión entonces!",
    alert_bad_login: "Datos de inicio de sesión incorrectos",
    alert_username_in_use: "El nombre de usuario ya está en uso",
    alert_password_mismatch: "Las contraseñas introducidas son diferentes",
    notification_login_success: "Has iniciado sesión correctamente"
  }
}

const toTranslate = document.querySelectorAll('[data-translate]')

function translate(lang) {
  const trans = translations[lang]
  toTranslate.forEach(e => e.textContent = trans[e.dataset.translate])

  localStorage.setItem('lang', lang)
}

function main() {
  translate(localStorage.getItem('lang') || 'es')

  const changeLangButtons = document.querySelectorAll('nav .dropdown-menu button')
  changeLangButtons.forEach(e => e.onclick = () => translate(e.dataset.lang))
}

main()