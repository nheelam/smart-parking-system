package com.example.smartparking.smartParking

import android.content.ContentValues
import android.graphics.Color
import android.os.Bundle
import android.os.Handler
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.databinding.DataBindingUtil
import com.example.smartparking.R
import com.example.smartparking.databinding.FragmentParkingBinding
import com.google.firebase.database.*
import com.jjoe64.graphview.series.DataPoint
import com.jjoe64.graphview.series.LineGraphSeries

class parkingFragment : Fragment() {

    private lateinit var binding: FragmentParkingBinding
    private lateinit var database : DatabaseReference
    private var curStatus = ""
    private var curStatus2 = 0

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        binding = DataBindingUtil.inflate<FragmentParkingBinding>(inflater, R.layout.fragment_parking, container, false)

        readData()
        writeGraph()


        return binding.root
    }

    private fun writeGraph() {
        database =
            FirebaseDatabase.getInstance("https://bait-2123-iot-g6-default-rtdb.asia-southeast1.firebasedatabase.app/")
                .getReference("smart_park")
        database.addValueEventListener(object : ValueEventListener {

            override fun onDataChange(dataSnapshot: DataSnapshot) {

                val temp = dataSnapshot.child("status").value

                curStatus = temp.toString()
                when (curStatus) {
                    "1A" -> {
                        curStatus2 = 1
                    }
                    "1B" -> {
                        curStatus2 = 1
                    }
                    "BothYes" -> {
                        curStatus2 = 2
                    }
                    "BothNo" -> {
                        curStatus2 = 0
                    }
                }
            }

            override fun onCancelled(error: DatabaseError) {
                // Failed to read value
                Log.w(ContentValues.TAG, "Failed to read value.", error.toException())
            }
        })
    }

    private fun DataPoint(x: Int, y: Int): DataPoint {
        return DataPoint(x.toDouble(), y.toDouble())
    }

    override fun onResume() {
        val graph = binding.graph2
        graph.viewport.setMinY(0.0)
        graph.viewport.setMaxY(3.0)
        graph.viewport.isScrollable = true
        graph.viewport.setScrollableY(true)
        graph.viewport.isYAxisBoundsManual = true

        graph.gridLabelRenderer.verticalAxisTitle = "Parked";
        graph.gridLabelRenderer.horizontalAxisTitle = "Time(s)";

        val series: LineGraphSeries<DataPoint> = LineGraphSeries(
            arrayOf(
                DataPoint(0,0)
            )
        )

        var time = 1
        var runnable: Runnable? = null
        Handler().postDelayed(Runnable{
            series.appendData(DataPoint(time, curStatus2), true, 90)
            series.thickness = 6
            series.color = Color.rgb(77, 150, 184)
            series.isDrawBackground = true
            series.backgroundColor = Color.rgb(77, 150, 184)

            graph.addSeries(series)

            time++

            Handler().postDelayed(runnable!!, 1000)
        }.also { runnable = it }, 1000)
        super.onResume()
    }

    private fun readData() {
        database =
            FirebaseDatabase.getInstance("https://bait-2123-iot-g6-default-rtdb.asia-southeast1.firebasedatabase.app/")
                .getReference("smart_park")
        database.addValueEventListener(object : ValueEventListener {

            override fun onDataChange(dataSnapshot: DataSnapshot) {

                val carStatus = dataSnapshot.child("status").value
                curStatus = carStatus.toString()


                when (curStatus) {
                    "1A" -> {
                        binding.colorPark1.setBackgroundResource(R.color.green)
                        binding.colorPark2.setBackgroundResource(R.color.red)
                        binding.tvPark1Status.setText("1A is available")
                        binding.tvPark2Status.setText("1B is not available")
                        binding.tvParkStatus.setText("Parking Slot: 1A")
                       /* binding.btnPark1.visibility = View.GONE
                        binding.btnPark2.visibility = View.VISIBLE
                        binding.imgPark1.visibility = View.GONE
                        binding.imgPark1.visibility = View.VISIBLE*/
                    }
                    "1B" -> {
                        binding.colorPark1.setBackgroundResource(R.color.red)
                        binding.colorPark2.setBackgroundResource(R.color.green)
                        binding.tvPark1Status.setText("1A is not available")
                        binding.tvPark2Status.setText("1B is available")
                        binding.tvParkStatus.setText("Parking Slot: 1B")
                       /* binding.btnPark1.visibility = View.VISIBLE
                        binding.btnPark2.visibility = View.GONE
                        binding.imgPark1.visibility = View.VISIBLE
                        binding.imgPark1.visibility = View.GONE*/
                    }
                    "BothYes" -> {
                        binding.colorPark1.setBackgroundResource(R.color.green)
                        binding.colorPark2.setBackgroundResource(R.color.green)
                        binding.tvPark1Status.setText("1A is available")
                        binding.tvPark2Status.setText("1B is available")
                        binding.tvParkStatus.setText("Parking Slot: All")
                       /* binding.btnPark1.visibility = View.GONE
                        binding.btnPark2.visibility = View.GONE
                        binding.imgPark1.visibility = View.GONE
                        binding.imgPark1.visibility = View.GONE*/
                    }
                    "BothNo" -> {
                        binding.colorPark1.setBackgroundResource(R.color.red)
                        binding.colorPark2.setBackgroundResource(R.color.red)
                        binding.tvPark1Status.setText("1A is not available")
                        binding.tvPark2Status.setText("1B is not available")
                        binding.tvParkStatus.setText("Parking Slot: None")
                        /*binding.btnPark1.visibility = View.VISIBLE
                        binding.btnPark2.visibility = View.VISIBLE
                        binding.imgPark1.visibility = View.VISIBLE
                        binding.imgPark1.visibility = View.VISIBLE*/
                    }
                    else -> {
                        print("")
                    }
                }
                //binding.tvPark1Status.text = curStatus.toString()
            }

            override fun onCancelled(error: DatabaseError) {
                // Failed to read value
                Log.w(ContentValues.TAG, "Failed to read value.", error.toException())
            }
        })
    }
}