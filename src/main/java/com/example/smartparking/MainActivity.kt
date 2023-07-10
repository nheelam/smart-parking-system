package com.example.smartparking

import android.app.NotificationChannel
import android.app.NotificationManager
import android.os.Build
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import androidx.annotation.RequiresApi
import androidx.databinding.DataBindingUtil
import androidx.navigation.Navigation
import androidx.navigation.findNavController
import androidx.navigation.fragment.findNavController
import androidx.navigation.ui.NavigationUI
import androidx.navigation.ui.setupActionBarWithNavController
import com.example.smartparking.databinding.ActivityMainBinding
import com.google.firebase.FirebaseApp
import com.google.firebase.database.DatabaseReference

import com.google.firebase.database.FirebaseDatabase




class MainActivity : AppCompatActivity() {

    private lateinit var binding:ActivityMainBinding
    private val nav by lazy{supportFragmentManager.findFragmentById(R.id.fragmentContainerView)!!.findNavController()}

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        //setContentView(R.layout.activity_main)
        binding = DataBindingUtil.setContentView(this, R.layout.activity_main)
        //val navController = this.findNavController(R.id.fragmentContainerView)
        //NavigationUI.setupActionBarWithNavController(this,navController)




        setupActionBarWithNavController(nav)


    }
    override fun onSupportNavigateUp(): Boolean {
        return nav.navigateUp() || super.onSupportNavigateUp()
    }
}