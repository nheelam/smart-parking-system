package com.example.smartparking.smartLight

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.ContentValues
import android.content.Context
import android.content.Intent
import android.os.Build
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.databinding.DataBindingUtil
import com.example.smartparking.MainActivity
import com.example.smartparking.R
import com.example.smartparking.databinding.FragmentLightBinding
import com.google.firebase.database.*

class lightFragment : Fragment() {

    private lateinit var binding : FragmentLightBinding
    private lateinit var database : DatabaseReference

    private val CHANNEL_ID = "channel_id_03"
    private val notificationId = 103

    private var curLight = 0
    private var curName = ""

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        binding = DataBindingUtil.inflate<FragmentLightBinding>(inflater, R.layout.fragment_light, container, false)

        createNotificationChannel()
        readData()

        return binding.root
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
            .setContentTitle("Car Park Payment")
            .setContentText("Payment Succeed")
            .setContentIntent(pendingIntent)
            .setPriority(NotificationCompat.PRIORITY_HIGH)

        with(NotificationManagerCompat.from(requireActivity())){
            notify(notificationId, builder.build())
        }
    }

    private fun readData() {
        database =
            FirebaseDatabase.getInstance("https://bait-2123-iot-g6-default-rtdb.asia-southeast1.firebasedatabase.app/")
                .getReference("Smart_Light")
        database.addValueEventListener(object : ValueEventListener {

            override fun onDataChange(dataSnapshot: DataSnapshot) {

                val alarm = dataSnapshot.child("light_sensor").value
                curLight = alarm.toString().toInt()

                val name = dataSnapshot.child("User").value
                curName = name.toString()

                if (curName != "Unknown"){
                    sendNotification()
                    binding.resultName.text = curName
                    binding.resultPayment.text = "Paid"
                } else {
                    binding.resultName.text = ""
                    binding.resultPayment.text = ""
                }


                if (curLight < 500){
                    binding.lightBackground.setBackgroundResource(R.color.green)
                } else {
                    binding.lightBackground.setBackgroundResource(R.color.red)
                }
            }

            override fun onCancelled(error: DatabaseError) {
                // Failed to read value
                Log.w(ContentValues.TAG, "Failed to read value.", error.toException())
            }
        })
    }
}