package com.example.netless;

import android.os.Handler;
import android.util.Log;
import java.io.IOException;
import java.net.ServerSocket;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

public class GroupOwnerSocketHandler extends Thread {
    ServerSocket socket = null;
    private final int THREAD_COUNT = 10;
    private Handler handler;
    private static final String TAG = "GroupOwnerSocketHandler";
    public GroupOwnerSocketHandler(Handler handler) throws IOException {
        try {
            socket = new ServerSocket(4545);
            this.handler = handler;
            Log.d("GroupOwnerSocketHandler", "Socket Started");
        } catch (IOException e) {
            e.printStackTrace();
            pool.shutdownNow();
            throw e;
        }
    }
    private final ThreadPoolExecutor pool = new ThreadPoolExecutor(
            THREAD_COUNT, THREAD_COUNT, 10, TimeUnit.SECONDS,
            new LinkedBlockingQueue<Runnable>());
    @Override
    public void run() {
        while (true) {
            try {
                // A blocking operation. Initiate a ChatManager instance when
                // there is a new connection
                pool.execute(new ChatManager(socket.accept(), handler));
                Log.d(TAG, "Launching the I/O handler");
            } catch (IOException e) {
                try {
                    if (socket != null && !socket.isClosed())
                        socket.close();
                } catch (IOException ioe) {
                }
                e.printStackTrace();
                pool.shutdownNow();
                break;
            }
        }
    }
}

//Esta clase implementa un servidor socket que escucha en el puerto 4545. El servidor socket
//espera conexiones entrantes y, cuando se establece una conexión, crea un nuevo hilo de ejecución
//para manejar la ejecución con el cliente.
