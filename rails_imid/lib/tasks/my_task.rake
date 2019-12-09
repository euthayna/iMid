namespace :mqtt do

  task subscribe: :environment do
    client = PahoMqtt::Client.new
    json = {}
    waiting_suback = true
    client.on_suback do
      waiting_suback = false
      puts "Subscribed"
    end

    message_counter = 0
    client.on_message do |message|
      puts "Message received on topic: #{message.topic}\n>>> #{message.payload}"
      json = message.payload
      hash = JSON.parse(json)

      case message.topic
      when 'metrics'
        puts 'Entrouuu'
        ::Metric.create!(
          sensor: hash["metrics"]["sensor"],
          value: hash["metrics"]["value"]
        )

      when 'release_code_request'
        code = ::Release.find_by(name: hash["name"], version: hash["version"])

        release_payload = {
          name: code.name,
          version: code.version,
          code: code.code
        }.to_json

        client.publish("release_code", release_payload, false, 1)

      when 'release_versions'

        # TODO last versions?
        code = ::Release.find_by(name: hash["name"], version: hash["version"])

        release_payload = {
          name: code.name,
          version: code.version,
          code: code.code
        }.to_json

        client.publish("release_code", release_payload, false, 1)

      else
        puts "Unknown topic"
      end

      message_counter += 1
    end

    client.connect(MQTT_HOST, 1883)

    client.subscribe(['metrics', 0])
    client.subscribe(['esp.init', 0])

    ### Waiting for the suback answer and excute the previously set on_suback callback
    while waiting_suback do
      sleep 0.01
    end
    # ### Waiting to assert that the message is displayed by on_message callback
    sleep 1

    while true do
      # puts "Retorno: #{json}" if json != {}
      # json
      # hash = JSON.parse(json)
      # ::Metric.create(sensor: hash["metrics"]["sensor"], value: hash["metrics"]["value"])
    end

    ### Calling an explicit disconnect
    client.disconnect

  end
end
