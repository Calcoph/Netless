package com.example.netless;

import android.os.Bundle;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

public class HomeActivity extends AppCompatActivity {
    public static final String TAG = "WiFiDirectChatHome";
    public SharedPreferences sharedpreferences;
    public static final String MyPREFERENCES = "MyPrefs" ;
    public static final String Name = "nameKey";
    public static String userName;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setTheme(R.style.AppTheme);
        setContentView(R.layout.activity_home);
        sharedpreferences = getSharedPreferences(MyPREFERENCES, Context.MODE_PRIVATE);

        userName = sharedpreferences.getString(Name, null);
        if(userName != null) {
            //Usuario anterior (antiguo)
            Log.i(TAG, "El alias del usuario es: " + sharedpreferences.getString(Name, null));
            gotoMainScreen();
        }

        Button saveUsername = findViewById(R.id.saveUsername);
        saveUsername.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                saveUsername();
            }
        });

    }

    private void saveUsername() {
        EditText userNameView = findViewById(R.id.userName);
        userName = userNameView.getText().toString();

        if (userName.isEmpty()){
            Toast.makeText(this, R.string.alias_introducido, Toast.LENGTH_LONG).show();
            return;
        }

        SharedPreferences.Editor editor = sharedpreferences.edit();
        editor.putString(Name, userName);
        editor.apply();
        Log.i(TAG, "Alias cambiado a: " + userName);
        Toast.makeText(this, R.string.alias_salvado, Toast.LENGTH_LONG).show();
        gotoMainScreen();
    }

    private void gotoMainScreen() {
        Intent intent = new Intent(this, WiFiServiceDiscoveryActivity.class);
        startActivity(intent);
    }
}

//Esta clase proporciona una interfaz de usuario para que el usuario ingrese un alias (nombre de usuario)
//y lo acabe guardando a través de un botón. Una vez guardado dicho alias, pasaremos a la página principal
//en donde se listarán los siguientes dispositivos.
