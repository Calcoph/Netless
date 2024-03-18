package com.netless.main

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class GUIPrincipal : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.principal)
    }

    fun abrirChat(id: String) {
        GUIChat(id)
    }

    fun abrirOpciones() {

    }

    fun aceptarUsuario(id: String) {
        val wl = Whitelist.getWhitelist()
        wl.anadirUsuario(id, applicationContext)
    }
}