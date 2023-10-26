const driveElements = document.querySelectorAll('.drive-element.folder > a')
console.log({driveElements})

driveElements.forEach(e => {
    e.onclick = (ev) => ev.preventDefault()
    e.ondblclick = () => window.location.href = e.getAttribute('href')
})