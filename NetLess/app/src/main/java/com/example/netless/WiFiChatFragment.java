package com.example.netless;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;

import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentActivity;
import android.content.Context;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

public class WiFiChatFragment extends Fragment {

    private View view;
    private ChatManager chatManager;
    private TextView chatLine;
    private ListView listView;
    ChatMessageAdapter adapter = null;
    private List<String> items = new ArrayList<String>();
    public SharedPreferences sharedpreferences;
    public static final String MyPREFERENCES = "MyPrefs" ;
    public static final String Name = "nameKey";
    private static final int FILE_REQUEST_CODE = 123;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,Bundle savedInstanceState) {
        sharedpreferences = this.getActivity().getSharedPreferences(MyPREFERENCES, Context.MODE_PRIVATE);
        view = inflater.inflate(R.layout.fragment_chat, container, false);
        chatLine = view.findViewById(R.id.txtChatLine);
        listView = view.findViewById(android.R.id.list);
        adapter = new ChatMessageAdapter(getActivity(), android.R.id.text1,
                items);
        listView.setAdapter(adapter);
        view.findViewById(R.id.button1).setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View arg0) {
                        if (chatManager != null) {
                            String userName = sharedpreferences.getString(Name, "UnKnown");
                            chatManager.write(userName + ": " + chatLine.getText().toString());
                            pushMessage("Yo: " + chatLine.getText().toString());
                            chatLine.setText("");
                            chatLine.clearFocus();
                        }
                    }
                });

        view.findViewById(R.id.buttonSendFiles).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Abre el explorador de archivos para seleccionar un archivo
                Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
                intent.setType("*/*");
                startActivityForResult(intent, FILE_REQUEST_CODE);
            }
        });
        return view;
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == FILE_REQUEST_CODE && resultCode == Activity.RESULT_OK) {
            Uri fileUri = data.getData();
            File selectedFile = new File(fileUri.getPath()); // Convertir la URI en un archivo
            chatManager.sendFile(selectedFile);
        }
    }
    public interface MessageTarget {
        public Handler getHandler();
    }

    public void setChatManager(ChatManager obj) {
        chatManager = obj;
    }

    public void pushMessage(String readMessage) {
        adapter.add(readMessage);
        adapter.notifyDataSetChanged();
    }
    public class ChatMessageAdapter extends ArrayAdapter<String> {
        List<String> messages = null;
        public ChatMessageAdapter(Context context, int textViewResourceId,
                                  List<String> items) {
            super(context, textViewResourceId, items);
        }
        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            View v = convertView;
            if (v == null) {
                LayoutInflater vi = (LayoutInflater) getActivity()
                        .getSystemService(Context.LAYOUT_INFLATER_SERVICE);
                v = vi.inflate(android.R.layout.simple_list_item_1, null);
            }
            String message = items.get(position);
            if (message != null && !message.isEmpty()) {
                TextView nameText = v.findViewById(android.R.id.text1);
                if (nameText != null) {
                    nameText.setText(message);
                    if (message.startsWith("Yo: ")) {
                        nameText.setTextAppearance(getActivity(),
                                R.style.normalText);
                    } else {
                        nameText.setTextAppearance(getActivity(),
                                R.style.boldText);
                    }
                }
            }
            return v;
        }
    }
}

