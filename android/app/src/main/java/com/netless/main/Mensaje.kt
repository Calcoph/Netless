package com.netless.main

class Mensaje(msg: String, dirección: Dirección) : Enviable(dirección) {
    val msg = msg
}