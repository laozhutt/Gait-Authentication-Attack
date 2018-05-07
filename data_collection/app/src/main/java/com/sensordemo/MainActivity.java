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
	 * ���ݶ���
	 */
	private List<SensorData> sensorDataList = new ArrayList<SensorData>();
	
	/**
	 * ��ʾ��ǰ�ռ�״̬��view
	 */
	private TextView stateView;
	/**
	 * ��ʾ��ǰ�ռ�������view
	 */
	private TextView numberView;
	/**
	 * ��ʾ��ǰ�ɼ������ֵ�view
	 */
	private  TextView participantView;
	/**
	 * ��ʼ�ͽ����İ�ť
	 */
	private Button startButton;

	/**
	 * ȷ�����ð�ť
	 */
	private Button configButton;

	/**
	 * ��������
	 */
	private EditText  etName;

	private String name;

	/**
	 * ��ʱ����ÿ10s�ռ�һ������
	 */
	private Timer timerAll;
	/**
	 * ��ʱ����ÿ10ms�ռ�һ������
	 */
	private Timer timer;
	/**
	 * �ظ�����
	 */
	private int repeatNum = 1;
	/**
	 * �ظ�����
	 */
	private int repeat = repeatNum;
	/**
	 * ÿ�����ݼ��ʱ��3600s
	 */
	private int timestamp = 3600000;
	/**
	 * ÿ�μ��10ms��100HZ
	 */
	private int interval = 10;
	/**
	 * ÿ�λ�1200s�ռ�����120000
	 */
	private int num = 120000;


	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		sensorManager = (SensorManager)getSystemService(Context.SENSOR_SERVICE);

		if(Environment.getExternalStorageState().equals(Environment.MEDIA_MOUNTED)) {
			Toast.makeText(getApplicationContext(), Environment.getExternalStorageDirectory().getPath(), Toast.LENGTH_SHORT).show();
			//SD����װ��
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
			//��ȡ��һ�����ٶȴ�������ֵ
			sensorData.accelerometerX = event.values[0];
			sensorData.accelerometerY = event.values[1];
			sensorData.accelerometerZ = event.values[2];
			break;
		case Sensor.TYPE_GYROSCOPE:
			//��ȡ��һ�������ǵ�ֵ
			sensorData.gyroscopeX = event.values[0];
			sensorData.gyroscopeY = event.values[1];
			sensorData.gyroscopeZ = event.values[2];
			break;
		case Sensor.TYPE_GRAVITY:
			//��ȡ��һ��������������ֵ
			sensorData.gravityX = event.values[0];
			sensorData.gravityY = event.values[1];
			sensorData.gravityZ = event.values[2];
			break;
		default:
			break;
		}
		//����UI�����ռ����ݵ�����
		numberView.setText(String.valueOf(sensorDataList.size()));
		if(repeat<=0){
			//������ֹͣ��������
			sensorManager.unregisterListener(this);
			stateView.setText("Idle");
			startButton.setText("Start");
			startButton.setEnabled(true);
			configButton.setEnabled(true);
			etName.setEnabled(true);
		}
	}
	
	/**
	 * ��һ�����ݱ��浽���������ݶ�����ȥ��ÿ10msһ��
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
		}, 5000); //ȥ��timestampzִ��һ��  }, 5000, timestamp);
	}
	
	/**
	 * ����������
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
	 * �����ʼ�ռ���ֹͣ�ռ�ʱ����
	 * 
	 */
	
	
	public void collect(View view){


		Button button = (Button) view;
		if(button.getText().equals("Stop")){
			//������ֹͣ��������
			sensorManager.unregisterListener(this);
			//ֹͣ������д�����
			timer.cancel();
			timerAll.cancel();
			//��¼����
			writeTxt();
			Log.e("stop","stop");
			//����UI
			stateView.setText("Idle");
			button.setText("Start");
			configButton.setEnabled(true);
			etName.setEnabled(true);
		}else{
			//���ٶȴ�������ʼ�ռ�����
			sensorManager.registerListener(this, 
					sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER), 
					SensorManager.SENSOR_DELAY_FASTEST);
			//�����ǿ�ʼ�ռ�����
			sensorManager.registerListener(this, 
					sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE), 
					SensorManager.SENSOR_DELAY_FASTEST);
			//������������ʼ�ռ�����
			sensorManager.registerListener(this, 
					sensorManager.getDefaultSensor(Sensor.TYPE_GRAVITY), 
					SensorManager.SENSOR_DELAY_FASTEST);
			//��ʼ����10msһ�ν�����д������
			saveData();
			
			stateView.setText("Collecting");
			button.setText("Stop");
			//button.setEnabled(false);
			configButton.setEnabled(false);
			etName.setEnabled(false);
		}
	}

	
	/**
	 * ������д��txt�ļ���
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
