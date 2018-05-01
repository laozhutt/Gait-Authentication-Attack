package com.sensordemo;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.util.ArrayList;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;

import android.app.Activity;
import android.app.ActivityManager;
import android.app.ActivityManager.RunningTaskInfo;
import android.content.ComponentName;
import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends Activity implements SensorEventListener{
	
	private SensorManager sensorManager;
	
	private SensorData sensorData = new SensorData();
	/**
	 * 数据队列
	 */
	private List<SensorData> sensorDataList = new ArrayList<SensorData>();
	
	/**
	 * 显示当前收集状态的view
	 */
	private TextView stateView;
	/**
	 * 显示当前收集条数的view
	 */
	private TextView numberView;
	/**
	 * 显示当前采集人名字的view
	 */
	private  TextView participantView;
	/**
	 * 开始和结束的按钮
	 */
	private Button startButton;

	/**
	 * 确认配置按钮
	 */
	private Button configButton;

	/**
	 * 配置姓名
	 */
	private EditText  etName;

	private String name;

	/**
	 * 计时器，每10s收集一组数据
	 */
	private Timer timerAll;
	/**
	 * 计时器，每10ms收集一次数据
	 */
	private Timer timer;
	/**
	 * 重复次数
	 */
	private int repeatNum = 1;
	/**
	 * 重复次数
	 */
	private int repeat = repeatNum;
	/**
	 * 每次数据间隔时间3600s
	 */
	private int timestamp = 3600000;
	/**
	 * 每次间隔10ms，100HZ
	 */
	private int interval = 10;
	/**
	 * 每次花1200s收集数据120000
	 */
	private int num = 120000;


	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		sensorManager = (SensorManager)getSystemService(Context.SENSOR_SERVICE);

		if(Environment.getExternalStorageState().equals(Environment.MEDIA_MOUNTED)) {
			Toast.makeText(getApplicationContext(), Environment.getExternalStorageDirectory().getPath(), Toast.LENGTH_SHORT).show();
			//SD卡已装入
		}
		else{
			Toast.makeText(getApplicationContext(), "no sdcard", Toast.LENGTH_SHORT).show();
		}
		
		stateView = (TextView) findViewById (R.id.state);
	
		numberView = (TextView) findViewById (R.id.number);
		participantView = (TextView)findViewById(R.id.participant);
		startButton = (Button) findViewById (R.id.bt_start);
		configButton = (Button) findViewById(R.id.config);
		etName = (EditText) findViewById(R.id.et_name);
		stateView.setText("Idle");
		numberView.setText("0");
		participantView.setText("");
		startButton.setEnabled(false);

		configButton.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View view) {
				String str = etName.getText().toString();
				etName.setText(null);
				if("".equals(str)){
					Toast.makeText(MainActivity.this,"name is empty", Toast.LENGTH_LONG).show();
				}
				else{
					Toast.makeText(MainActivity.this,"name: "+str, Toast.LENGTH_LONG).show();
					name = str;
					participantView.setText(name);
					startButton.setEnabled(true);
				}


			}
		});

	}

	@Override
	public void onSensorChanged(SensorEvent event) {
		
		switch(event.sensor.getType()){
		case Sensor.TYPE_ACCELEROMETER:
			//获取到一个加速度传感器的值
			sensorData.accelerometerX = event.values[0];
			sensorData.accelerometerY = event.values[1];
			sensorData.accelerometerZ = event.values[2];
			break;
		case Sensor.TYPE_GYROSCOPE:
			//获取到一个陀螺仪的值
			sensorData.gyroscopeX = event.values[0];
			sensorData.gyroscopeY = event.values[1];
			sensorData.gyroscopeZ = event.values[2];
			break;
		case Sensor.TYPE_GRAVITY:
			//获取到一个重力传感器的值
			sensorData.gravityX = event.values[0];
			sensorData.gravityY = event.values[1];
			sensorData.gravityZ = event.values[2];
			break;
		default:
			break;
		}
		//更新UI中已收集数据的条数
		numberView.setText(String.valueOf(sensorDataList.size()));
		if(repeat<=0){
			//传感器停止返回数据
			sensorManager.unregisterListener(this);
			stateView.setText("Idle");
			startButton.setText("Start");
			startButton.setEnabled(true);
			configButton.setEnabled(true);
			etName.setEnabled(true);
		}
	}
	
	/**
	 * 将一条数据保存到传感器数据队列中去，每10ms一次
	 */
	private void saveData(){
		repeat = repeatNum;
		timerAll = new Timer();
		timerAll.schedule(new TimerTask(){

			@Override
			public void run() {
				timer = new Timer();
				timer.schedule(new TimerTask(){

					@Override
					public void run() {				
						SensorData data = new SensorData();
						data.currentTime = System.currentTimeMillis();
						data.accelerometerX = sensorData.accelerometerX;
						data.accelerometerY = sensorData.accelerometerY;
						data.accelerometerZ = sensorData.accelerometerZ;
						data.gravityX = sensorData.gravityX;
						data.gravityY = sensorData.gravityY;
						data.gravityZ = sensorData.gravityZ;
						data.gyroscopeX = sensorData.gyroscopeX;
						data.gyroscopeY = sensorData.gyroscopeY;
						data.gyroscopeZ = sensorData.gyroscopeZ;
						sensorDataList.add(data);



						if(sensorDataList.size()>=num){
							Log.e("wait","wait");
							timer.cancel();
							writeTxt();
							if(--repeat<=0){
								timerAll.cancel();
							}
						}
					}
				}, interval, interval);
			}
		}, 5000); //去掉timestampz执行一次  }, 5000, timestamp);
	}
	
	/**
	 * 传感器数据
	 */
	private class SensorData{
		public long currentTime;
		public float accelerometerX;
		public float accelerometerY;
		public float accelerometerZ;
		public float gyroscopeX;
		public float gyroscopeY;
		public float gyroscopeZ;
		public float gravityX;
		public float gravityY;
		public float gravityZ;
	}

	@Override
	public void onAccuracyChanged(Sensor sensor, int accuracy) {
		
	}
	
	/**
	 * 点击开始收集和停止收集时调用
	 * 
	 */
	
	
	public void collect(View view){


		Button button = (Button) view;
		if(button.getText().equals("Stop")){
			//传感器停止返回数据
			sensorManager.unregisterListener(this);
			//停止将数据写入队列
			timer.cancel();
			timerAll.cancel();
			//记录数据
			writeTxt();
			Log.e("stop","stop");
			//更新UI
			stateView.setText("Idle");
			button.setText("Start");
			configButton.setEnabled(true);
			etName.setEnabled(true);
		}else{
			//加速度传感器开始收集数据
			sensorManager.registerListener(this, 
					sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER), 
					SensorManager.SENSOR_DELAY_FASTEST);
			//陀螺仪开始收集数据
			sensorManager.registerListener(this, 
					sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE), 
					SensorManager.SENSOR_DELAY_FASTEST);
			//重力传感器开始收集数据
			sensorManager.registerListener(this, 
					sensorManager.getDefaultSensor(Sensor.TYPE_GRAVITY), 
					SensorManager.SENSOR_DELAY_FASTEST);
			//开始按照10ms一次将数据写进队列
			saveData();
			
			stateView.setText("Collecting");
			button.setText("Stop");
			//button.setEnabled(false);
			configButton.setEnabled(false);
			etName.setEnabled(false);
		}
	}

	
	/**
	 * 将数据写到txt文件中
	 * 
	 */
	public void writeTxt(){
		
		String dir = Environment.getExternalStorageDirectory().getPath()+"/SensorDemoData/";
		File fileDir = new File(dir);
		if(!fileDir.exists()){
			fileDir.mkdir();
		}
		String dir2 = Environment.getExternalStorageDirectory().getPath()+"/SensorDemoData/" + name;
		File fileDir2 = new File(dir2);
		if(!fileDir2.exists()){
			fileDir2.mkdir();
		}
		try {
			String path = Environment.getExternalStorageDirectory().getPath()+"/SensorDemoData/"+name+"/"+System.currentTimeMillis()+".txt";
			File file = new File(path);
			Writer writer = new FileWriter(file,true);
			for(SensorData sensorData : sensorDataList){
//				Double ad = Math.sqrt(sensorData.accelerometerX*sensorData.accelerometerX+
//						sensorData.accelerometerY*sensorData.accelerometerY+
//						sensorData.accelerometerZ*sensorData.accelerometerZ);
				String string = sensorData.currentTime+"\n"+
								sensorData.accelerometerX+"\n"+
								sensorData.accelerometerY+"\n"+
								sensorData.accelerometerZ+"\n"+
								sensorData.gyroscopeX+"\n"+
								sensorData.gyroscopeY+"\n"+
								sensorData.gyroscopeZ+"\n"+
								sensorData.gravityX+"\n"+
								sensorData.gravityY+"\n"+
								sensorData.gravityZ+"\n";
				writer.write(string);
			}
			writer.close();
			sensorDataList.clear();
			
//			path = Environment.getExternalStorageDirectory().getPath()+"/SensorDemoData/name"+System.currentTimeMillis()+".txt";
//			file = new File(path);
//			writer = new FileWriter(file,true);
//			for(String packName : packNameList){
//				packName = packName+"\n";
//				writer.write(packName);
//			}
//			writer.close();
//			packNameList.clear();

		} catch (IOException e) {
			
			e.printStackTrace();
		}
	}
	


}
