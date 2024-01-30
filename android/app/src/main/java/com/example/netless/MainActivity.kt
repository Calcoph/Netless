package com.example.netless

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View.OnClickListener
import android.widget.Button

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main);
        val button = findViewById<Button>(R.id.button2);

        button.setOnClickListener {
            val intent = Intent(this, Chat::class.java);
            startActivity(intent);
        }
    }
}