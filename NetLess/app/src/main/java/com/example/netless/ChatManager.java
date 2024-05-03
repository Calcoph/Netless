package com.example.netless;


import android.os.Handler;
import android.util.Log;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

public class ChatManager implements Runnable {

    private static final String TAG = "ChatHandler";

    private Socket socket = null;
    private Handler handler;
    private InputStream iStream;
    private OutputStream oStream;

    public ChatManager(Socket socket, Handler handler) {
        this.socket = socket;
        this.handler = handler;
    }

    @Override
    public void run() {
        try {
            iStream = socket.getInputStream();
            oStream = socket.getOutputStream();
            byte[] buffer = new byte[1024];
            int bytes;
            handler.obtainMessage(WiFiServiceDiscoveryActivity.MY_HANDLE, this).sendToTarget();
            while (true) {
                try {
                    // Read from the InputStream
                    bytes = iStream.read(buffer);
                    if (bytes == -1) {
                        break;
                    }
                    // Send the obtained bytes to the UI Activity
                    Log.d(TAG, "Rec:" + String.valueOf(buffer));
                    handler.obtainMessage(WiFiServiceDiscoveryActivity.MESSAGE_READ, bytes, -1, buffer).sendToTarget();
                } catch (IOException e) {
                    Log.e(TAG, "desconectado", e);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                socket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    public void write(String msg) {
        final byte[] buffer = msg.getBytes();
        Thread thread = new Thread() {
            public void run() {
                try {
                    oStream.write(buffer);
                } catch (IOException e) {
                    Log.e(TAG, "Excepción de escritura", e);
                }
            }
        };
        thread.start();
    }

    public void sendFile(File file) {
        try {
            // Obtener el nombre del archivo
            String fileName = file.getName();
            // Obtener los datos del archivo
            byte[] fileData = new byte[(int) file.length()];
            FileInputStream fileInputStream = new FileInputStream(file);
            fileInputStream.read(fileData);
            fileInputStream.close();

            // Enviar primero la longitud del nombre del archivo
            byte[] fileNameLength = new byte[4]; // int tiene 4 bytes
            fileNameLength[0] = (byte) (fileName.length() >> 24);
            fileNameLength[1] = (byte) (fileName.length() >> 16);
            fileNameLength[2] = (byte) (fileName.length() >> 8);
            fileNameLength[3] = (byte) (fileName.length());
            oStream.write(fileNameLength);

            // Enviar el nombre del archivo
            oStream.write(fileName.getBytes());
            // Enviar los datos del archivo
            oStream.write(fileData);

        } catch (IOException e) {
            Log.e(TAG, "Error al enviar el archivo", e);
        }
    }
}

/*Esta clase maneja la comunicación de la red y las operaciones de escritura y transferencia.*/