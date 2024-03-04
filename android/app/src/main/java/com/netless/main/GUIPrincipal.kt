package com.netless.main

class GUIPrincipal {
    fun abrir_chat(id: String) {
        GUIChat(id)
    }

    fun abrir_opciones() {

    }

    fun aceptar_usuario(id: String) {
        var wl = Whitelist.get_whitelist()
        wl.añadir_usuario(id)
    }
}