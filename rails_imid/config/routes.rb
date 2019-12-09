Rails.application.routes.draw do
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
  # get 'releases/index'
  resources :releases
  resources :metrics, only: [:index, :destroy]

  root 'releases#index'
end
