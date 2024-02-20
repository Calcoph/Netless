package com.example.netless

class HistorialChat {
    val listaEnviables = ArrayList<Enviable>()

    fun añadir_enviable(enviable: Enviable, id_usuario: String) {
        listaEnviables.add(enviable)
    }

    fun mostrar_en_pantalla() {

    }
}