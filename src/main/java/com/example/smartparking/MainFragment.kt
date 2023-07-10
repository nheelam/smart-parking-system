package com.example.smartparking

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import androidx.databinding.DataBindingUtil
import androidx.navigation.Navigation
import androidx.navigation.findNavController
import androidx.navigation.fragment.findNavController
import com.example.smartparking.databinding.FragmentMainBinding
import com.google.android.gms.common.util.DataUtils
import com.google.firebase.database.FirebaseDatabase

class MainFragment : Fragment() {
    private lateinit var binding: FragmentMainBinding

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        //val view = inflater.inflate(R.layout.fragment_main, container, false)
        binding = DataBindingUtil.inflate(inflater, R.layout.fragment_main, container, false)

        //val btnParking = view.findViewById<Button>(R.id.btnParking)
        //val btnTemp = view.findViewById<Button>(R.id.btnTemp)
        //binding.btnRegister.setOnClickListener() {requireView().findNavController().navigate(R.id.action_mainFragment_to_registerFragment)}
        binding.btnParking.setOnClickListener() {requireView().findNavController().navigate(R.id.action_mainFragment_to_parkingFragment)}
        binding.btnTemp.setOnClickListener() {requireView().findNavController().navigate(R.id.action_mainFragment_to_temperatureFragment)}
        binding.btnLight.setOnClickListener() {requireView().findNavController().navigate(R.id.action_mainFragment_to_lightFragment)}
        binding.btnAlarm.setOnClickListener() {requireView().findNavController().navigate(R.id.action_mainFragment_to_alarmFragment)}

        return binding.root
    }
}