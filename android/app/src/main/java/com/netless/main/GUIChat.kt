package com.netless.main

import android.content.Context
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.TextView
import com.google.android.material.textfield.TextInputEditText
import java.io.File

class GUIChat(id: String) : AppCompatActivity() {
    val usuario: Usuario
    init {
        val usuarios = ListaUsuarios.get_lista()
        usuario = usuarios.obtener_usuario(id)!!
        val nombre = usuario.obtener_nombre()
        val chat = usuario.obtener_chat()
        chat.mostrar_en_pantalla()
        if (usuario.acepta_conexiones()) {
            activar_envio()
        } else {
            desactivar_envio()
            if (usuario.solicitar_conexion()) {
                activar_envio()
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.chat)
    }

    fun enviar_mensaje(context: Context) {
        val textbox = findViewById<TextInputEditText>(R.id.textInputEditText)
        val msg = textbox.text.toString()
        usuario.enviar_mensaje(msg, context)
    }

    fun enviar_fichero(context: Context) {
        val fich = seleccionar_fichero()
        val nombre = fich.name
        val tamaño = fich.totalSpace

        usuario.obtener_confirmacion(nombre, tamaño)
        usuario.enviar_fichero(fich, context)
    }

    fun activar_envio() {

    }

    fun desactivar_envio() {

    }

    fun eliminar_de_whitelist(context: Context) {
        val id = usuario.obtener_id()
        val wl = Whitelist.get_whitelist()
        wl.quitar_usuario(id, context)
    }

    fun seleccionar_fichero(): File {

    }
}
