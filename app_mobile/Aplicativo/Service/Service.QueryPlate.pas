unit Service.QueryPlate;

interface

uses
  System.SysUtils, FMX.Graphics, Model.QueryPlate, Proxy.QueryPlate;

type
  TQueryPlateService = class
  private
    Froxy: TQueryPlateProxy;
  public
    constructor Create();
    destructor Destroy(); override;

    procedure Query(const AImg: TBitmap; ACallback: TProc<TQueryPlateModel>);
  end;

implementation

uses
  System.Threading;

{ TQueryVehicle }

constructor TQueryPlateService.Create;
begin
  Froxy := TQueryPlateProxy.Create(nil);
end;

destructor TQueryPlateService.Destroy;
begin
  Froxy.DisposeOf();
  inherited;
end;

procedure TQueryPlateService.Query(const AImg: TBitmap; ACallback: TProc<TQueryPlateModel>);
begin
  Froxy.SendRequest(AImg, ACallback);
end;

end.
