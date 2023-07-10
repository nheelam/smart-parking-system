package com.example.smartparking.registration

import android.content.ContentValues
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.databinding.DataBindingUtil
import com.example.smartparking.R
import com.example.smartparking.databinding.FragmentRegisterBinding
import com.example.smartparking.registration.model.User
import com.google.firebase.database.*
import com.google.firebase.storage.FirebaseStorage
import com.google.firebase.database.DataSnapshot
import java.nio.file.Files.exists


class registerFragment : Fragment() {

    private lateinit var binding:FragmentRegisterBinding
    private lateinit var database : DatabaseReference
    private var dataExist: Boolean = false
    var name: String = ""
    var plateNum: String = ""
    var contact: String = ""
    var pin: String = ""

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        binding = DataBindingUtil.inflate<FragmentRegisterBinding>(inflater, R.layout.fragment_register, container, false)

        binding.btnRegisterUser.setOnClickListener() {

            //registerUser(name, plateNum, contact, pin)
            dataExist = false

            name = binding.tfName.text.toString()
            plateNum = binding.tfPlateNumber.text.toString()
            contact = binding.tfContact.text.toString()
            pin = binding.tfPin.text.toString()

            validateUser(plateNum)

            if (dataExist){
                Toast.makeText(requireActivity(), "Plate Number already registered", Toast.LENGTH_SHORT).show()
            } else {
                registerUser(name, plateNum, contact, pin)
            }
        }

        return binding.root
    }

    private fun registerUser(name: String, plateNum: String, contact: String, pin: String) {
        //dataExist = false
        /*val name = binding.tfName.text.toString()
        val plateNum = binding.tfPlateNumber.text.toString()
        val contact = binding.tfContact.text.toString()
        val pin = binding.tfPin.text.toString()*/

        val user = User(name, plateNum, contact, pin)

        if (name.isEmpty() || plateNum.isEmpty() || contact.isEmpty()) {
            Toast.makeText(
                requireActivity(),
                "Please enter the require information",
                Toast.LENGTH_SHORT
            ).show()
            return
        }
        /*database =
            FirebaseDatabase.getInstance("https://bait-2123-iot-g6-default-rtdb.asia-southeast1.firebasedatabase.app/")
                .getReference("user_registered")
        database.addListenerForSingleValueEvent(object : ValueEventListener {
            override fun onDataChange(snapshot: DataSnapshot) {
                if (snapshot.child(plateNum).exists()) {
                    Toast.makeText(requireActivity(), "exists!", Toast.LENGTH_SHORT).show()
                    dataExist = true
                    return
                }

            }

            override fun onCancelled(error: DatabaseError) {
                Log.d("registerFragment", "Failed to read data")
            }
        })
*/

        Log.d("RegisterActivity", "Name is: " + name)
        Log.d("RegisterActivity", "Plate Number is: " + plateNum)
        Log.d("RegisterActivity", "Contact is: " + contact)

        database =
            FirebaseDatabase.getInstance("https://bait-2123-iot-g6-default-rtdb.asia-southeast1.firebasedatabase.app/")
                .getReference("user_registered")


        database.child(plateNum).setValue(user)
            .addOnSuccessListener {
                Log.d("registerFragment", "Successfully created user")
                Toast.makeText(requireActivity(), "Successfully created user", Toast.LENGTH_SHORT)
                    .show()
            }
            .addOnFailureListener {
                Log.d("registerFragment", "Failed to create user")
                Toast.makeText(requireActivity(), "Failed to create user", Toast.LENGTH_SHORT)
                    .show()
            }
        }

    private fun validateUser(plateNum: String) {
        dataExist = false

        database =
            FirebaseDatabase.getInstance("https://bait-2123-iot-g6-default-rtdb.asia-southeast1.firebasedatabase.app/")
                .getReference("user_registered")
        database.addValueEventListener(object: ValueEventListener{
            override fun onDataChange(snapshot: DataSnapshot) {
                if(snapshot.hasChild(plateNum)){
                    Toast.makeText(requireActivity(), "exists!", Toast.LENGTH_SHORT).show()
                    trueFalse()
                }
            }

            override fun onCancelled(error: DatabaseError) {
                Log.d("registerFragment", "Failed to read data")

            }
        })
    }

    private fun trueFalse(){
        dataExist = true
    }
}