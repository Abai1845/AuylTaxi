import os

files = {
    ".github/workflows/android_build.yml": """name: Build AuylTaxi APK

on:
  push:
    branches: [ "main" ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@v3
        with:
          gradle-version: '8.4'

      - name: Build Debug APK
        run: gradle assembleDebug

      - name: Upload APK Artifact
        uses: actions/upload-artifact@v4
        with:
          name: AuylTaxi-APK
          path: app/build/outputs/apk/debug/app-debug.apk
""",

    "settings.gradle": """pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "AuylTaxi"
include ':app'
""",

    "build.gradle": """plugins {
    id 'com.android.application' version '8.2.0' apply false
}
""",

    "gradle.properties": """org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
android.nonTransitiveRClass=true
""",

    "app/build.gradle": """plugins {
    id 'com.android.application'
}

android {
    namespace 'kz.auyltaxi.app'
    compileSdk 34

    defaultConfig {
        applicationId "kz.auyltaxi.app"
        minSdk 23
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }

    buildTypes {
        release {
            minifyEnabled false
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'org.osmdroid:osmdroid-android:6.1.18'
}
""",

    "app/src/main/AndroidManifest.xml": """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />

    <application
        android:allowBackup="true"
        android:label="AuylTaxi"
        android:supportsRtl="true"
        android:theme="@style/Theme.AppCompat.Light.NoActionBar">
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
""",

    "app/src/main/res/layout/activity_main.xml": """<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#F5F5F5">

    <org.osmdroid.views.MapView
        android:id="@+id/mapView"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:layout_above="@+id/bottomPanel" />

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:padding="12dp"
        android:gravity="end">

        <Button
            android:id="@+id/btnToggleFriends"
            android:layout_width="wrap_content"
            android:layout_height="42dp"
            android:text="👥 Достар"
            android:textSize="13sp"
            android:backgroundTint="#1976D2"
            android:textColor="#FFFFFF"
            android:layout_marginEnd="8dp"/>

        <Button
            android:id="@+id/btnNightMode"
            android:layout_width="wrap_content"
            android:layout_height="42dp"
            android:text="🌙 Түнгі"
            android:textSize="13sp"
            android:backgroundTint="#263238"
            android:textColor="#FFFFFF"/>
    </LinearLayout>

    <LinearLayout
        android:id="@+id/bottomPanel"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_alignParentBottom="true"
        android:orientation="vertical"
        android:background="#FFFFFF"
        android:elevation="12dp"
        android:padding="16dp">

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:background="#FFF8E1"
            android:padding="10dp"
            android:gravity="center_vertical"
            android:layout_marginBottom="12dp">

            <LinearLayout
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:orientation="vertical">

                <TextView
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:text="🚕 Қалаға (500 тг / адам)"
                    android:textStyle="bold"
                    android:textSize="16sp"
                    android:textColor="#212121"/>

                <TextView
                    android:id="@+id/tvCityTaxiStatus"
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:text="Қызыл Кобальт: 3/4 адам жиналды (1 орын бос)"
                    android:textSize="13sp"
                    android:textColor="#D84315"
                    android:layout_marginTop="2dp"/>
            </LinearLayout>

            <Button
                android:id="@+id/btnJoinCityTaxi"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="Орын алу"
                android:backgroundTint="#FF8F00"
                android:textColor="#FFFFFF"/>
        </LinearLayout>

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Ауыл ішінде қайда барасыз?"
            android:textStyle="bold"
            android:textSize="15sp"
            android:textColor="#424242"
            android:layout_marginBottom="6dp"/>

        <HorizontalScrollView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:scrollbars="none"
            android:layout_marginBottom="10dp">

            <LinearLayout
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:orientation="horizontal">

                <Button
                    android:id="@+id/btnPlaceSchool"
                    android:layout_width="wrap_content"
                    android:layout_height="44dp"
                    android:text="🏫 Мектеп"
                    android:backgroundTint="#ECEFF1"
                    android:textColor="#212121"
                    android:layout_marginEnd="6dp"/>

                <Button
                    android:id="@+id/btnPlaceCenter"
                    android:layout_width="wrap_content"
                    android:layout_height="44dp"
                    android:text="🛒 Орталық дүкен"
                    android:backgroundTint="#ECEFF1"
                    android:textColor="#212121"
                    android:layout_marginEnd="6dp"/>

                <Button
                    android:id="@+id/btnPlaceHospital"
                    android:layout_width="wrap_content"
                    android:layout_height="44dp"
                    android:text="🏥 Аурухана"
                    android:backgroundTint="#ECEFF1"
                    android:textColor="#212121"
                    android:layout_marginEnd="6dp"/>

                <Button
                    android:id="@+id/btnPlaceMill"
                    android:layout_width="wrap_content"
                    android:layout_height="44dp"
                    android:text="🌾 Төменгі шет"
                    android:backgroundTint="#ECEFF1"
                    android:textColor="#212121"/>
            </LinearLayout>
        </HorizontalScrollView>

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:layout_marginBottom="12dp">

            <CheckBox
                android:id="@+id/cbMultiplePeople"
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:text="2-3 адамбыз"
                android:textSize="14sp"/>

            <CheckBox
                android:id="@+id/cbHasCargo"
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:text="📦 Үлкен зат/қап бар"
                android:textSize="14sp"/>
        </LinearLayout>

        <Button
            android:id="@+id/btnCallTaxi"
            android:layout_width="match_parent"
            android:layout_height="56dp"
            android:text="ТАКСИ ШАҚЫРУ (Жүргізушімен келісу)"
            android:textSize="15sp"
            android:textStyle="bold"
            android:backgroundTint="#2E7D32"
            android:textColor="#FFFFFF"/>

    </LinearLayout>
</RelativeLayout>
""",

    "app/src/main/java/kz/auyltaxi/app/MainActivity.java": """package kz.auyltaxi.app;

import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.Uri;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import org.osmdroid.config.Configuration;
import org.osmdroid.tileprovider.tilesource.TileSourceFactory;
import org.osmdroid.util.GeoPoint;
import org.osmdroid.views.MapView;
import org.osmdroid.views.overlay.Marker;
import org.osmdroid.views.overlay.TilesOverlay;

public class MainActivity extends AppCompatActivity {

    private MapView mapView;
    private boolean isNightMode = false;
    private boolean showFriends = true;
    private String selectedDestination = "Таңдалмады";
    private int currentPassengers = 3;
    private Marker friendMarker;
    private final String TAXI_DRIVER_PHONE = "+77071234567";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Context ctx = getApplicationContext();
        Configuration.getInstance().load(ctx, PreferenceManager.getDefaultSharedPreferences(ctx));
        setContentView(R.layout.activity_main);

        mapView = findViewById(R.id.mapView);
        mapView.setTileSource(TileSourceFactory.MAPNIK);
        mapView.setMultiTouchControls(true);

        GeoPoint auylCenter = new GeoPoint(43.238949, 76.889709);
        mapView.getController().setZoom(16.0);
        mapView.getController().setCenter(auylCenter);

        setupMapMarkers(auylCenter);
        setupButtons();
    }

    private void setupMapMarkers(GeoPoint center) {
        Marker redCobalt = new Marker(mapView);
        redCobalt.setPosition(new GeoPoint(center.getLatitude() + 0.0012, center.getLongitude() + 0.0015));
        redCobalt.setTitle("🔴 Қызыл Кобальт (Ерлан)");
        redCobalt.setSnippet("Статус: Қалаға жинап тұр (3/4 орын) | 500 тг");
        redCobalt.setOnMarkerClickListener((marker, mapView) -> {
            marker.showInfoWindow();
            showDriverChatDialog("Ерлан (Қызыл Кобальт)", "+77071112233");
            return true;
        });
        mapView.getOverlays().add(redCobalt);

        Marker whiteNiva = new Marker(mapView);
        whiteNiva.setPosition(new GeoPoint(center.getLatitude() - 0.0015, center.getLongitude() - 0.0010));
        whiteNiva.setTitle("⚪ Ақ Нива (Сәкен аға)");
        whiteNiva.setSnippet("Статус: Ауыл ішінде БОС (Жүк салуға болады)");
        whiteNiva.setOnMarkerClickListener((marker, mapView) -> {
            marker.showInfoWindow();
            showDriverChatDialog("Сәкен аға (Ақ Нива)", "+77074445566");
            return true;
        });
        mapView.getOverlays().add(whiteNiva);

        friendMarker = new Marker(mapView);
        friendMarker.setPosition(new GeoPoint(center.getLatitude() + 0.0005, center.getLongitude() - 0.0020));
        friendMarker.setTitle("👋 Досың: Мақсат");
        friendMarker.setSnippet("Орталық дүкеннің қасында жүр");
        mapView.getOverlays().add(friendMarker);
    }

    private void setupButtons() {
        Button btnNightMode = findViewById(R.id.btnNightMode);
        Button btnToggleFriends = findViewById(R.id.btnToggleFriends);
        Button btnJoinCityTaxi = findViewById(R.id.btnJoinCityTaxi);
        TextView tvCityTaxiStatus = findViewById(R.id.tvCityTaxiStatus);

        Button btnSchool = findViewById(R.id.btnPlaceSchool);
        Button btnCenter = findViewById(R.id.btnPlaceCenter);
        Button btnHospital = findViewById(R.id.btnPlaceHospital);
        Button btnMill = findViewById(R.id.btnPlaceMill);

        CheckBox cbMultiple = findViewById(R.id.cbMultiplePeople);
        CheckBox cbCargo = findViewById(R.id.cbHasCargo);
        Button btnCallTaxi = findViewById(R.id.btnCallTaxi);

        btnNightMode.setOnClickListener(v -> {
            isNightMode = !isNightMode;
            if (isNightMode) {
                mapView.getOverlayManager().getTilesOverlay().setColorFilter(TilesOverlay.INVERT_COLORS);
                btnNightMode.setText("☀️ Күндізгі");
            } else {
                mapView.getOverlayManager().getTilesOverlay().setColorFilter(null);
                btnNightMode.setText("🌙 Түнгі");
            }
            mapView.invalidate();
        });

        btnToggleFriends.setOnClickListener(v -> {
            showFriends = !showFriends;
            friendMarker.setEnabled(showFriends);
            mapView.invalidate();
            Toast.makeText(this, showFriends ? "Достар картада көрінеді" : "Достар жасырылды", Toast.LENGTH_SHORT).show();
        });

        btnJoinCityTaxi.setOnClickListener(v -> {
            if (currentPassengers < 4) {
                currentPassengers++;
                tvCityTaxiStatus.setText("Қызыл Кобальт: 4/4 ТОЛДЫ! Жолға шығуда...");
                tvCityTaxiStatus.setTextColor(Color.parseColor("#2E7D32"));
                btnJoinCityTaxi.setText("Толды");
                btnJoinCityTaxi.setEnabled(false);
                showDriverChatDialog("Ерлан (Қызыл Кобальт - Қалаға)", TAXI_DRIVER_PHONE);
            }
        });

        btnSchool.setOnClickListener(v -> selectPlace("Мектеп"));
        btnCenter.setOnClickListener(v -> selectPlace("Орталық дүкен"));
        btnHospital.setOnClickListener(v -> selectPlace("Аурухана"));
        btnMill.setOnClickListener(v -> selectPlace("Төменгі шет"));

        btnCallTaxi.setOnClickListener(v -> {
            if (selectedDestination.equals("Таңдалмады")) {
                Toast.makeText(this, "Алдымен баратын жерді батырмадан таңдаңыз!", Toast.LENGTH_SHORT).show();
                return;
            }
            String peopleInfo = cbMultiple.isChecked() ? "2-3 адам" : "1 адам";
            String cargoInfo = cbCargo.isChecked() ? "Үлкен зат/қап бар" : "Жүк жоқ";
            String orderMessage = "АуылТакси тапсырыс:\\n📍 Қайда: " + selectedDestination +
                    "\\n👥 Саны: " + peopleInfo + "\\n📦 Жүк: " + cargoInfo + "\\n(Бағасын келісеміз)";
            sendOrderHybrid(orderMessage, TAXI_DRIVER_PHONE);
        });
    }

    private void selectPlace(String place) {
        selectedDestination = place;
        Toast.makeText(this, "Таңдалды: " + place, Toast.LENGTH_SHORT).show();
    }

    private void showDriverChatDialog(String driverName, String phone) {
        new AlertDialog.Builder(this)
                .setTitle(driverName)
                .setMessage("Жүргізушімен тікелей байланысып, нақты тұрған жеріңіз бен бағасын келісіңіз:")
                .setPositiveButton("💬 Чатқа жазу (WhatsApp)", (dialog, which) ->
                        openWhatsAppChat(phone, "Ассалаумағалейкум! Такси бос па? Бағыт: " + selectedDestination))
                .setNeutralButton("📩 SMS жіберу (Сет жоқ болса)", (dialog, which) ->
                        openSms(phone, "Такси керек. Бағыт: " + selectedDestination))
                .setNegativeButton("Жабу", null)
                .show();
    }

    private void sendOrderHybrid(String message, String phone) {
        if (isInternetAvailable()) {
            openWhatsAppChat(phone, message);
        } else {
            Toast.makeText(this, "Интернет әлсіз. Тапсырыс SMS арқылы жіберіледі!", Toast.LENGTH_LONG).show();
            openSms(phone, message);
        }
    }

    private void openWhatsAppChat(String phone, String message) {
        try {
            String url = "https://api.whatsapp.com/send?phone=" + phone + "&text=" + Uri.encode(message);
            startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url)));
        } catch (Exception e) {
            openSms(phone, message);
        }
    }

    private void openSms(String phone, String message) {
        Intent smsIntent = new Intent(Intent.ACTION_SENDTO, Uri.parse("smsto:" + phone));
        smsIntent.putExtra("sms_body", message);
        startActivity(smsIntent);
    }

    private boolean isInternetAvailable() {
        ConnectivityManager cm = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo activeNetwork = cm.getActiveNetworkInfo();
        return activeNetwork != null && activeNetwork.isConnected();
    }

    @Override
    protected void onResume() {
        super.onResume();
        mapView.onResume();
    }

    @Override
    protected void onPause() {
        super.onPause();
        mapView.onPause();
    }
}
"""
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ AuylTaxi жобасының барлық файлдары сәтті құрылды!")
