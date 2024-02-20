package com.example.netless

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle

class GUIChat(id: String) : AppCompatActivity() {
    val usuario: Usuario
    init {
        val usuarios = ListaUsuarios

    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.chat)
    }
}
