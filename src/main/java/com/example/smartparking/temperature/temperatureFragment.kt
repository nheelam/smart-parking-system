package com.example.smartparking.temperature

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.ContentValues
import android.content.Context
import android.content.Intent
import android.graphics.BitmapFactory
import android.graphics.Color
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.core.content.ContextCompat.getSystemService
import com.example.smartparking.MainActivity
import com.example.smartparking.databinding.FragmentTemperatureBinding
import com.google.firebase.database.*
import com.jjoe64.graphview.series.DataPoint
import com.jjoe64.graphview.series.LineGraphSeries

class temperatureFragment : Fragment() {
    private lateinit var binding : FragmentTemperatureBinding
    private lateinit var database : DatabaseReference

    private val CHANNEL_ID = "channel_id_01"
    private val notificationId = 101

    private var curTemp = 0
    private var curHum = 0

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        binding = FragmentTemperatureBinding.inflate(inflater, container, false)

        createNotificationChannel()
        readData()
        writeGraph()

        return binding.root
    }

    private fun DataPoint(x: Int, y: Int): DataPoint {
        return DataPoint(x.toDouble(), y.toDouble())
    }

    private fun readData() {
        database =
            FirebaseDatabase.getInstance("https://bait-2123-iot-g6-default-rtdb.asia-southeast1.firebasedatabase.app/")
                .getReference("Smart_Temperature")
        database.addValueEventListener(object : ValueEventListener {

            override fun onDataChange(dataSnapshot: DataSnapshot) {

                val temp = dataSnapshot.child("temp").value
                val hum = dataSnapshot.child("hum").value
                curTemp = temp.toString().toInt()

                if (curTemp > 80){
                    sendNotification()
                }

                curHum = hum.toString().toInt()
                binding.tvHum.text = hum.toString()
                binding.tvTemp.text = temp.toString()
            }

            override fun onCancelled(error: DatabaseError) {
                // Failed to read value
                Log.w(ContentValues.TAG, "Failed to read value.", error.toException())
            }
        })
    }

    override fun onResume() {
        val graph = binding.graph
        graph.viewport.setMinY(0.0)
        graph.viewport.setMaxY(100.0)
        graph.viewport.isScrollable = true
        graph.viewport.setScrollableY(true)
        graph.viewport.isYAxisBoundsManual = true

        graph.gridLabelRenderer.verticalAxisTitle = "Temperature";
        graph.gridLabelRenderer.horizontalAxisTitle = "Time(s)";

        val series: LineGraphSeries<DataPoint> = LineGraphSeries(
            arrayOf(
                DataPoint(0,0)
            )
        )

        val series2: LineGraphSeries<DataPoint> = LineGraphSeries(
            arrayOf(
                DataPoint(0,0)
            )
        )

        var time = 1
        var runnable: Runnable? = null
        Handler().postDelayed(Runnable{
            series.appendData(DataPoint(time, curTemp), true, 90)
            series.thickness = 6
            series.color = Color.rgb(77, 150, 184)
            series.isDrawBackground = true
            series.backgroundColor = Color.rgb(77, 150, 184)

            graph.addSeries(series)

            series2.appendData(DataPoint(time, curHum), true, 90)
            series2.thickness = 6
            series2.color = Color.rgb(124, 252, 0)
            series2.isDrawBackground = true
            series2.backgroundColor = Color.rgb(124, 252, 0)

            graph.addSeries(series2)
            time++

            Handler().postDelayed(runnable!!, 1000)
        }.also { runnable = it }, 1000)
        super.onResume()
    }

    private fun writeGraph() {
        database =
            FirebaseDatabase.getInstance("https://bait-2123-iot-g6-default-rtdb.asia-southeast1.firebasedatabase.app/")
                .getReference("Smart_Temperature")
        database.addValueEventListener(object : ValueEventListener {

            override fun onDataChange(dataSnapshot: DataSnapshot) {

                val temp = dataSnapshot.child("temp").value
                val hum = dataSnapshot.child("hum").value

                curTemp = temp.toString().toInt()
                curHum = hum.toString().toInt()
            }

            override fun onCancelled(error: DatabaseError) {
                // Failed to read value
                Log.w(ContentValues.TAG, "Failed to read value.", error.toException())
            }
        })
    }

    private fun createNotificationChannel(){
        if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.O){
            val name = "Notification Title"
            val descriptionText = "Notification Description"
            val importance = NotificationManager.IMPORTANCE_DEFAULT
            val channel = NotificationChannel(CHANNEL_ID, name, importance).apply {
                description = descriptionText
            }
            val notificationManager: NotificationManager = requireActivity().getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
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
            .setSmallIcon(R.drawable.notification_icon_background)
            .setContentTitle("Warning: High Temperature")
            .setContentText("Your parking lot is on fire")
            .setContentIntent(pendingIntent)
            .setPriority(NotificationCompat.PRIORITY_HIGH)

        with(NotificationManagerCompat.from(requireActivity())){
            notify(notificationId, builder.build())
        }
    }
}