unit Service.QueryDetran;

interface

uses
  System.SysUtils, Proxy.QueryDetran, Model.QueryDetran;

type
  TQueryDetranService = class
  private
    Froxy: TQueryDetranProxy;
  public
    constructor Create();
    destructor Destroy(); override;

    procedure Query(const APlate: string; ACallback: TProc<TQueryDetranModel>);
  end;

implementation

{ TQueryDetranService }

constructor TQueryDetranService.Create;
begin
  Froxy := TQueryDetranProxy.Create(nil);
end;

destructor TQueryDetranService.Destroy;
begin
  Froxy.DisposeOf();
  inherited;
end;

procedure TQueryDetranService.Query(const APlate: string; ACallback: TProc<TQueryDetranModel>);
begin
  Froxy.SendRequest(APlate, ACallback);
end;

end.
