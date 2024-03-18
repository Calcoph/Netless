package com.netless.main

class Mensaje(private val msg: String, direccion: Direccion) : Enviable(direccion) {
    fun getMsg(): String {
        return msg
    }
}