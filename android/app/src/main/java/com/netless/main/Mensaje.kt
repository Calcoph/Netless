package com.example.netless

class Mensaje(msg: String, dirección: Dirección) : Enviable(dirección) {
    val msg = msg
}