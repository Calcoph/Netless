package com.netless.main

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class GUIPrincipal : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.principal)
    }

    fun abrir_chat(id: String) {
        GUIChat(id)
    }

    fun abrir_opciones() {

    }

    fun aceptar_usuario(id: String) {
        var wl = Whitelist.get_whitelist()
        wl.añadir_usuario(id, applicationContext)
    }
}