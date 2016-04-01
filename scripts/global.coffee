readCookie = (name) ->
    nameEQ = name + "="
    ca = document.cookie.split(';')
    for c in ca
        while c.charAt(0) == ' '
            c = c.substring(1, c.length)
        if c.indexOf(nameEQ) == 0
            return c.substring(nameEQ.length, c.length)
    return null
window.readCookie = readCookie

createCookie = (name, value, days) ->
    if days
        date = new Date()
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000))
        expires = "; expires=" + date.toGMTString()
    else
        expires = "; expires=Thu, 01-Jan-1970 00:00:01 GMT"
    document.cookie = name + "=" + value + expires + "; path=/"
window.createCookie = createCookie

dataURItoBlob = (uri) ->
    byteString = atob(uri.split(',')[1])
    mimeString = uri.split(',')[0].split(':')[1].split(':')[0]
    ab = new ArrayBuffer(byteString.length)
    ia = new Uint8Array(ab)
    for i in [0 .. byteString.length]
        ia[i] = byteString.charCodeAt(i)
    return new Blob([ ab ], { type: 'image/png' })
window.dataURItoBlob = dataURItoBlob

s4 = -> Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1)

guid = -> s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4()
window.guid = guid

window.getPosition = (e) ->
    x = 0
    y = 0
    while true
        x += e.offsetLeft
        y += e.offsetTop
        break if e.offsetParent == null
        e = e.offsetParent
    return [x, y]

window.addEventListener('DOMContentLoaded', (e) ->
    link.addEventListener('click', (e) ->
        e.preventDefault()
        if readCookie('ad-opt-out')
            e.target.textContent = 'opt-out'
            a.textContent = 'opted-in' for a in document.querySelectorAll('.ad-state')
            createCookie('ad-opt-out', '', -1)
        else
            e.target.textContent = 'opt-in'
            a.textContent = 'opted-out' for a in document.querySelectorAll('.ad-state')
            createCookie('ad-opt-out', 1, 3650)
        ad.innerHTML = "Sorry! You won't see any ads again. If you change your mind, <a href='/advertising'>opt-in here</a>." for ad in document.querySelectorAll('.advertisement')
    , false) for link in document.querySelectorAll('.ad-opt-out')
, false)
