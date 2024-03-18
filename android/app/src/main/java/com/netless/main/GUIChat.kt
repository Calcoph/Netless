package com.netless.main

import android.content.Context
import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import com.google.android.material.textfield.TextInputEditText
import java.io.File

class GUIChat(id: String) : AppCompatActivity() {
    private val usuario: Usuario
    init {
        val usuarios = ListaUsuarios.getLista()
        usuario = usuarios.obtenerUsuario(id)!!
        val nombre = usuario.obtenerNombre()
        val chat = usuario.obtenerChat()
        chat.mostrarEnPantalla()
        if (usuario.aceptaConexiones()) {
            activarEnvio()
        } else {
            desactivarEnvio()
            if (usuario.solicitarConexion()) {
                activarEnvio()
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.chat)
    }

    fun enviarMensaje(context: Context) {
        val textbox = findViewById<TextInputEditText>(R.id.textInputEditText)
        val msg = textbox.text.toString()
        usuario.enviarMensaje(msg, context)
    }

    fun enviarFichero(context: Context) {
        //val fich = seleccionar_fichero()
        val fich = File("") // TODO: get an actual file
        val nombre = fich.name
        val tamano = fich.totalSpace

        usuario.obtenerConfirmacion(nombre, tamano)
        usuario.enviarFichero(fich, context)
    }

    fun activarEnvio() {

    }

    fun desactivarEnvio() {

    }

    fun eliminarDeWhitelist(context: Context) {
        val id = usuario.obtenerId()
        val wl = Whitelist.getWhitelist()
        wl.quitarUsuario(id, context)
    }

    fun seleccionarFichero() {
        val intent = Intent().setType("*/*").setAction(Intent.ACTION_GET_CONTENT)
        startActivity(intent)
    }
}
