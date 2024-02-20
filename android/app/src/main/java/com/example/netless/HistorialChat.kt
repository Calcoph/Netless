package com.example.netless

class HistorialChat {
    val listaEnviables = ArrayList<Enviable>()

    fun añadir_fichero(fichero: Fichero, id_usuario: String) {
        añadir_enviable(fichero)

        fichero.get_nombre()
        fichero.get_fecha()
        fichero.get_direccion()

        "INSERT INTO Fichero(nombre) VALUES (${nombre})"
        "INSERT INTO Enviable(fecha, direccion, fich_id) VALUES (now(), ${direccion}, ${fich_id}"
        "SELECT chat_id FROM Usuario WHERE id=${id_usuario}"
        "INSERT INTO Enviables(chat_id, env_id) VALUES (${chat_id}, ${env_id})"
    }

    fun añadir_mensaje(mens: Mensaje, id_usuario: String) {
        añadir_enviable(mens)

        "INSERT INTO Mensaje VALUES mens"
        "INSERT INTO Enviable VALUES fecha_date, direccion"
    }

    private fun añadir_enviable(enviable: Enviable) {
        listaEnviables.add(enviable)
        mostrar_en_pantalla()
    }

    fun mostrar_en_pantalla() {
        for (enviable in listaEnviables) {
            enviable.mostrar_en_pantalla()
        }
    }
}