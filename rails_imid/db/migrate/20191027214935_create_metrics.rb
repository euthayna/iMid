class CreateMetrics < ActiveRecord::Migration[5.2]
  def change
    create_table :metrics do |t|
      t.string :sensor
      t.string :value

      t.timestamps
    end
  end
end
