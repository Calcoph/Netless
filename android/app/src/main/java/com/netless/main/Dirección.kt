package com.netless.main

enum class Direccion {
    Entrante {
        override fun toInt() = 1
    },
    Saliente {
        override fun toInt() = 2
    };

    abstract fun toInt(): Int
    fun fromInt(int: Int): Direccion? {
        return when(int) {
            1 -> Entrante
            2 -> Saliente
            else -> null
        }
    }
}