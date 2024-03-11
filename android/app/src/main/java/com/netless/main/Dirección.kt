package com.netless.main

enum class Dirección {
    Entrante {
        override fun toInt() = 1
    },
    Saliente {
        override fun toInt() = 2
    };

    abstract fun toInt(): Int
    fun fromInt(int: Int): Dirección? {
        return when(int) {
            1 -> Dirección.Entrante
            2 -> Dirección.Saliente
            else -> null
        }
    }
}