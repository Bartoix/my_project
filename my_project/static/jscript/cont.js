function alertare() {


    let myform = document.forms['formular']
    mesaj = ''

    if (myform['nume'].value === '') {
        mesaj += 'Numele nu poate fi nul\n'
    }

    if (myform['mail'].value === '') {
        mesaj += 'Email-ul nu poate fi nul\n'
    }

    if (myform['echipa'].value === '') {
        mesaj += 'Va rugam, introduceti echipa favorita\n'

    }

    if (myform['mesaj'].value === '') {
        mesaj += 'Mesajul nu poate fi nul'
    }

    if (mesaj != '') {
        alert(mesaj)
    }
}