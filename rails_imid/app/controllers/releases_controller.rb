class ReleasesController < ApplicationController
  def index
    @releases = Release.all
  end

  def show
    @release = Release.find(params[:id])
  end

  def new
    last_release = Release.last
    @release = Release.new(name: last_release.name, code: last_release.code)
    Rails.logger.info "wtf #{@release.inspect}"
  end

  def create
    @release = Release.new(release_params)
    @release.save

    client = PahoMqtt::Client.new
    client.connect(MQTT_HOST, 1883)
    release_payload = {
      name: @release.name,
      version: @release.version,
      code: @release.code
    }.to_json
    Rails.logger.info "Pushing code: "
    Rails.logger.info release_payload
    client.publish("release_code", release_payload, false, 0)
    sleep(2)
    client.disconnect

    redirect_to @release
  end

  def edit
  end

  def update
  end

  def destroy
    @release = Release.find(params[:id])
    @release.destroy
    redirect_to releases_path
  end

  private

  def release_params
    params.require(:release).permit(:name, :version, :code)
      .tap do |ppp|
        ppp['code'].strip();
      end
  end
end
