const toastElements = document.querySelectorAll('.toast')
const toastList = [...toastElements].map(toast => new bootstrap.Toast(toast))

toastList.forEach(toast => toast.show())