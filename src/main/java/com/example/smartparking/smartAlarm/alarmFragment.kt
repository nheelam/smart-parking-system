package com.example.smartparking.smartAlarm

import android.Manifest
import android.app.*
import android.content.ContentValues
import android.content.ContentValues.TAG
import android.content.Context
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.databinding.DataBindingUtil
import com.example.smartparking.R
import com.example.smartparking.databinding.FragmentAlarmBinding
import com.example.smartparking.databinding.FragmentParkingBinding
import com.example.smartparking.databinding.FragmentTemperatureBinding
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.util.Log
import android.widget.Toast
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.work.Data
import com.example.smartparking.MainActivity
import com.google.firebase.database.*
import com.google.firebase.storage.FirebaseStorage
import java.net.URI
import java.util.*

class alarmFragment : Fragment() {

    private lateinit var binding : FragmentAlarmBinding
    val REQUEST_CODE = 100
    private lateinit var ImageUri: Uri
    private lateinit var database : DatabaseReference

    private val CHANNEL_ID = "channel_id_02"
    private val notificationId = 102

    private var curAlarm = 0

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        binding = DataBindingUtil.inflate<FragmentAlarmBinding>(inflater, R.layout.fragment_alarm, container, false)

        createNotificationChannel()
        readData()

        binding.btnUpload.setOnClickListener {
            pickImageFromGallery()

        }

        return binding.root
    }

    private fun pickImageFromGallery() {
        val intent= Intent(Intent.ACTION_PICK)
        intent.type= "image/*"
        startActivityForResult(intent, IMAGE_PICK_CODE)
    }

    companion object {
        private val IMAGE_PICK_CODE = 1000;
        private val PERMISSION_CODE = 1001;
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        ImageUri = data?.data!!
        binding.imgPlateNumber.setImageURI(data?.data)

        uploadImage()
    }

    private fun uploadImage(){
        val filename = "test.jpeg"
        val storageReference =
            FirebaseStorage.getInstance("gs://bait-2123-iot-g6.appspot.com")
                .getReference("image/$filename")

        storageReference.putFile(ImageUri)
        binding.alarmNote.setText("Note: The problem you faced is already reported to the service center.")
    }


    private fun createNotificationChannel(){
        if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.O){
            val name = "Notification Title"
            val descriptionText = "Notification Description"
            val importance = NotificationManager.IMPORTANCE_DEFAULT
            val channel = NotificationChannel(CHANNEL_ID, name, importance).apply {
                description = descriptionText
            }
            val notificationManager: NotificationManager = requireActivity().getSystemService(
                Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.createNotificationChannel(channel)
        }
    }
    private fun sendNotification() {
        val intent = Intent(requireActivity(), MainActivity::class.java).apply{
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
        }
        val pendingIntent: PendingIntent = PendingIntent.getActivity(requireActivity(),0,intent,0)
        //val bitmap = BitmapFactory.decodeResource(requireActivity().resources, R.drawable.common_full_open_on_phone)

        val builder = NotificationCompat.Builder(requireActivity(), CHANNEL_ID)
            .setSmallIcon(com.google.firebase.database.R.drawable.notification_icon_background)
            .setContentTitle("Warning: Alarm is on")
            .setContentText("Your parking lot's alarm is on")
            .setContentIntent(pendingIntent)
            .setPriority(NotificationCompat.PRIORITY_HIGH)

        with(NotificationManagerCompat.from(requireActivity())){
            notify(notificationId, builder.build())
        }
    }

    private fun readData() {
        database =
            FirebaseDatabase.getInstance("https://bait-2123-iot-g6-default-rtdb.asia-southeast1.firebasedatabase.app/")
                .getReference("Smart_Alarm")
        database.addValueEventListener(object : ValueEventListener {

            override fun onDataChange(dataSnapshot: DataSnapshot) {

                val alarm = dataSnapshot.child("Status").value
                curAlarm = alarm.toString().toInt()

                //binding.resultPlateNumber.text = alarm.toString()

                if (curAlarm == 1){
                    sendNotification()
                    binding.alarmBackground.setBackgroundResource(R.color.red)
                } else {
                    binding.alarmBackground.setBackgroundResource(R.color.green)
                }
            }

            override fun onCancelled(error: DatabaseError) {
                // Failed to read value
                Log.w(ContentValues.TAG, "Failed to read value.", error.toException())
            }
        })
    }
}

