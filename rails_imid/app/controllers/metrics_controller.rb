class MetricsController < ApplicationController
  def index
    @metrics = Metric.all
  end

  def destroy
    @metric = Metric.find(params[:id])
    @metric.destroy
    redirect_to metrics_path
  end
end
