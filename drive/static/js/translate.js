const translations = {
  en: {
    lang: "Language",
    logout: "Logout",
    drive_shared: "Shared",
    drive_mydrive: "My drive",
    drive_path_not_found: "The path you requested was not found",
    drive_file_uploaded: "Files have been uploaded successfully",
    drive_folder_created: "The folder has been created successfully",
    drive_folder_exists: "This folder already exists. Please, choose another name",
    drive_item_delete: "The item has been deleted successfully",
    drive_item_rename: "The item has been renamed successfully",
    upload_file_btn: "Upload files",
    upload_file_title: "Upload some new files",
    upload_file_desc: "Choose the files you want to upload:",
    new_folder_btn: "New folder",
    new_folder_title: "Create a new folder",
    new_folder_desc: "Name of the folder you want to create:",
    delete_item_btn: "Delete",
    delete_item_title: "Delete item",
    delete_item_desc: "Are you sure you want to delete",
    cancel_btn: "Cancel",
    rename_item_btn: "Rename",
    rename_item_title: "Rename item",
    rename_item_desc: "Set the new name for",
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
    notification_login_success: "You have logged in successfully!",
    notification_signup_success: "You have signed up successfully!"
  },
  es: {
    lang: "Idioma",
    logout: "Cerrar sesión",
    drive_shared: "Compartido",
    drive_mydrive: "Mi unidad",
    drive_path_not_found: "El directorio al que intentas acceder no se ha encontrado",
    drive_file_uploaded: "Los archivos se han subido correctamente",
    drive_folder_created: "La carpeta se ha creado correctamente",
    drive_folder_exists: "Esta carpeta ya exise. Porfavor, elige otro nombre",
    drive_item_delete: "El elemento se ha eliminado correctamente",
    drive_item_rename: "El elemento se ha modificado correctamente",
    upload_file_btn: "Subir archivos",
    upload_file_title: "Sube nuevos archivos",
    upload_file_desc: "Elige los archivos que quieres subir:",
    new_folder_btn: "Nueva carpeta",
    new_folder_title: "Crea una nueva carpeta",
    new_folder_desc: "Nombre de la carpeta que quieres crear:",
    delete_item_btn: "Eliminar",
    delete_item_title: "Eliminar elemento",
    delete_item_desc: "¿Estás seguro de que quieres eliminar",
    cancel_btn: "Cancelar",
    rename_item_btn: "Renombrar",
    rename_item_title: "Cambio de nombre",
    rename_item_desc: "Introduce el nuevo nombre para",
    username: "Usuario",
    password: "Contraseña",
    repeat_password: "Repetir contraseña",
    remember: "Recuérdame",
    login_title: "Inicia sesión en tu cuenta",
    login_btn: "Inicar sesión",
    login_redirect: "¿No tienes una cuenta todavía?",
    login_redirect_url: "¡Regístrate ahora!",
    signup_title: "Crea una nueva cuenta",
    signup_btn: "Registrarse",
    signup_redirect: "¿Ya tienes una cuenta?",
    signup_redirect_url: "¡Inicia sesión entonces!",
    alert_bad_login: "Datos de inicio de sesión incorrectos",
    alert_username_in_use: "El nombre de usuario ya está en uso",
    alert_password_mismatch: "Las contraseñas introducidas son diferentes",
    notification_login_success: "Has iniciado sesión correctamente!",
    notification_signup_success: "Te has registrado correctamente!"
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